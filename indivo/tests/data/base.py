class TestModel(object):
    model_fields = [] # A list of field names needed to construct a Django Model
    model_class = None # The Django Model Subclass to construct

    def __getattribute__(self, item):
        """Lookup foreign keys"""
        ret = super(TestModel, self).__getattribute__(item)
        if isinstance(ret, Key):
            ret = getattr(ret, Key.TO)
        return ret

    def __setattr__(self, item, value):
        """Update our django_object whenever our fields get updated. Don't update foreignKeys until save."""
        if hasattr(self, 'django_obj') and item in self.model_fields and not isinstance(value, Key):
            setattr(self.django_obj, item, value)
            self.dirty = True
        elif isinstance(value, Key):
            self.dirty = True
        return super(TestModel, self).__setattr__(item, value)

    def build_django_obj(self):
        model_args = {}
        for f in self.model_fields:
            field_val = self.__dict__[f]
            if not isinstance(field_val, Key):
                model_args[f] = field_val
                
        self.django_obj = self.model_class(**model_args)

    def update(self, attr_dict, **other_attrs):
        attr_dict.update(other_attrs)
        for attr, val in attr_dict.iteritems():
            setattr(self, attr, val)

    def save(self):

        # Make sure we've built the object to save
        if not hasattr(self, 'django_obj') or not self.django_obj:
            self.build_django_obj()

        # Have we ever saved before?
        resave = self.django_obj.pk

        # Is our object currently represented in the DB?
        in_db = self.model_class.objects.filter(pk=self.django_obj.pk).exists()

        # Save if our object is dirty, or if the DB obj was yanked out from under us (i.e., by a tearDown method)
        if not hasattr(self, 'dirty') or self.dirty or (resave and not in_db):
            
            # If we aren't in the database, make sure we get a new pk on save
            if not in_db:
                self.django_obj.pk = ''

            # Mark as not dirty, so foreign keys don't recurse forever
            self.dirty = False

            # Save our foreign keys first, and add them to our django_obj
            for attrname, attrval in self.__dict__.iteritems():
                if isinstance(attrval, Key):
                    attrval.save()
                    setattr(self.django_obj, attrname, attrval.as_django())

            # Save our django object
            self.django_obj.save()

class Key(object):
    TO = 'to'
    INDEX_ARG = 'index_arg'

    def __init__(self, module_name, list_name, index_arg):
        self.module_name = module_name
        self.list_name = list_name
        setattr(self, self.INDEX_ARG, index_arg)

    def __getattr__(self, item):
        if item == self.TO:
            model_list = self._import_to_list()
            to = self.process_model_list(model_list)
            setattr(self, self.TO, to)
            return to
        else:
            to = getattr(self, self.TO)
            return getattr(to, item)

    def _import_to_list(self):
        m = __import__(self.module_name, globals(), locals(), [self.list_name], -1)
        return getattr(m, self.list_name)

    def as_django(self):
        """ Should return the django_objects underlying the test_objects linked to by the Key"""
        pass

    def process_model_list(self, model_list):
        """ Should Return the test_object{s} linked to by the Key, given a list of models and 
            the self.INDEX_ARG. """
        pass
    
    def save(self):
        """ Should call save on each model in self.TO """
        pass

class ForeignKey(Key):
    def process_model_list(self, model_list):
        return model_list[getattr(self, self.INDEX_ARG)]

    def save(self):
        getattr(self, self.TO).save()

    def as_django(self):
        to = getattr(self, self.TO)
        if not hasattr(to, 'django_obj'):
            to.build_django_obj()
        return to.django_obj

class ManyToManyKey(Key):
    def process_model_list(self, model_list):
        return [model_list[i] for i in getattr(self, self.INDEX_ARG)]

    def save(self):
        for model in getattr(self, self.TO):
            model.save()

    def as_django(self):
        ret = []
        for model in getattr(self, self.TO):
            if not hasattr(model, 'django_obj'):
                model.build_django_obj()
            ret.append(model.django_obj)
        return ret

def raw_data_to_objs(data_list, target_object):
    return [target_object(**raw_data) for raw_data in data_list]
