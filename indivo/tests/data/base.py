import copy

__all__ = [
    'TestDataContext',
    'TestModel',
    'TestDataItem',
    'scope',
    'ForeignKey',
    'ManyToManyKey',
]

class TestDataContext(object):
    MARKED = 'marked'

    def __init__(self):
        self.subcontexts = [{}]

    def tdi_id(self, tdi):
        """ Get a unique id for the test_data. This is composed of two things:
            the actual id() of the list that it came from, and the index in that
            list. If we have a lazy item, we'll have to de-ref it here. """
        if tdi.lazy:
            tdi._get_data_list()
        return '%s_%s'%(str(id(tdi.data_list)),
                        str(tdi.index))        

    def del_model(self, test_data_id, subcontext_id):
        subcontext = self.subcontexts[subcontext_id]
        if subcontext.has_key(test_data_id):
            del subcontext[test_data_id]
        else:
            raise ValueError('No such model')

    def _add_subcontext(self):
        # DISABLED, FOR NOW
        # self.subcontexts.append({})
        return len(self.subcontexts) - 1

    def _add_model(self, test_data_item, subcontext_id, **overrides):
        
        test_model_id = self.tdi_id(test_data_item)

        # Look for the desired model in our subcontext
        subcontext = self.subcontexts[subcontext_id]

        # First time we've ever seen this model: Mark for processing
        if not subcontext.has_key(test_model_id):
            subcontext[test_model_id] = self.MARKED
            
        # We've seen this model before, but it hasn't been fully saved yet
        # Ideally, we would handle this behavior in a sophisticated way
        # (i.e. add ourself to a queue for later processing).
        # But this is just test data, after all, and these chains can only 
        # occur if the test data is created with circular foreignkey references,
        # so let's just complain.
        elif subcontext[test_model_id] == self.MARKED:
            raise Exception('Circular references in test data: can\'t save test items.')
    
        # We've seen this model before, and it has been fully saved: just return it.
        else:
            return subcontext[test_model_id]

        # create the model, with info that points to this specific subcontext
        raw_data_dict = copy.deepcopy(test_data_item.raw_data)
        raw_data_dict.update(identifier=test_model_id, context=self, subcontext_id=subcontext_id)
        raw_data_dict.update(overrides)
        test_model = test_data_item.tm_subclass(**raw_data_dict)

        # register it with our subcontext, now that processing is done
        subcontext[test_model_id] = test_model
        return test_model

    def add_key(self, key, from_instance):
        subcontext_id = from_instance.subcontext_id
        try:
            ret = []
            for test_data_item in key.to:
                ret.append(self._add_model(test_data_item, subcontext_id))
            return ret
        except TypeError:
            return self._add_model(key.to, subcontext_id)

    def add_model(self, test_data_item, **overrides):
        subcontext_id = self._add_subcontext()
        return self._add_model(test_data_item, subcontext_id, **overrides)

class TestModel(object):
    model_fields = [] # A list of field names needed to construct a Django Model
    model_class = None # The Django Model Subclass to construct

    def __init__(self, identifier, context, subcontext_id, **subclass_args):
        self.identifier = identifier
        self.context = context
        self.subcontext_id = subcontext_id
        self._setupargs(**subclass_args)
        self.marked_for_save = False

    def _setupargs(self, **subclass_args):
        """ Should be overriden by subclasses to take initialization args 
            and set up the subclass model. """
        raise NotImplementedError

    def update(self, field_dict, **fields):
        field_dict.update(fields)
        for k, v in field_dict.iteritems():
            setattr(self, k, v)

    def __setattr__(self, item, value):
        """Update our django_object whenever our fields get updated. Follow foreignKeys. """

        # setup foreign keys
        self_attr_val, django_obj_attr_val = self._foreign_key_check(value)

        # update the django object
        if hasattr(self, 'django_obj') and item in self.model_fields:
            setattr(self.django_obj, item, django_obj_attr_val)
            self.dirty = True

        return super(TestModel, self).__setattr__(item, self_attr_val)

    def _foreign_key_check(self, field):
        if isinstance(field, ForeignKey):
            tm = self.context.add_key(field, self)
            return (tm, tm.save())
        elif isinstance(field, TestModel):
            return (field, field.save())
        elif isinstance(field, ManyToManyKey):
            tms = self.context.add_key(field, self)
            return (tms, [tm.save() for tm in tms])
        elif isinstance(field, list) and field and isinstance(field[0], TestModel):
            return (field, [tm.save() for tm in field])
        return (field, field)

    def build_django_obj(self):
        # handle foreign keys
        model_args = dict([(f, self._foreign_key_check(getattr(self, f))[1]) for f in self.model_fields])
        self.django_obj = self.model_class(**model_args)

    def save(self):

        # Make sure we've built the object to save
        dobj_p = getattr(self, 'django_obj', False)
        if not dobj_p:
            self.build_django_obj()

        # Save our django object
        dirty_p = getattr(self, 'dirty', True)
        if dirty_p:
            self.django_obj.save()
            self.dirty = False

        return self.django_obj

class TestDataItem(object):
    def __init__(self, index, module_name=None, list_name=None, data_list=None, lazy=False):
        self.index = index
        self.lazy = lazy
        if lazy:
            self.module_name = module_name
            self.list_name = list_name
            self.data_list = None            
        else:
            self.data_list = data_list

    def _get_data_list(self):
        self.data_list = getattr(__import__(self.module_name, globals(), locals(), [self.list_name], -1), self.list_name)

    @property
    def tm_subclass(self):
        if self.data_list is None:
            self._get_data_list()
        return self.data_list.model_class

    @property
    def raw_data(self):
        if self.data_list is None:
            self._get_data_list()
        return self.data_list[self.index]

def scope(raw_list, tm_subclass):

    class TestModelScopedList(list):
        def __init__(self, tm_subclass, *args, **kwargs):
            self.model_class = tm_subclass
            return super(TestModelScopedList, self).__init__(*args, **kwargs)

        def __add__(self, other):
            """ Allow concatenation of multiple scoped lists with the same tm_subclass. """
            other_model_class = getattr(other, 'model_class', None)
            if other_model_class and other_model_class == self.model_class:
                return TestModelScopedList(self.model_class, super(TestModelScopedList, self).__add__(other))
            else:
                raise TypeError('Can only concatenate TestModelScopedLists with the same TestModel subclasses')

    return TestModelScopedList(tm_subclass, raw_list)

class Key(object):
    def __init__(self, module_name, list_name, index_arg):
        self.module_name = module_name
        self.list_name = list_name
        self.index_arg = index_arg

    @property
    def to(self):
        """ Should return the raw TestDataIdentifier(s) pointed to by the key. """
        raise NotImplementedError

class ForeignKey(Key):

    @property
    def to(self):
        return TestDataItem(self.index_arg, module_name=self.module_name, list_name=self.list_name, lazy=True)

class ManyToManyKey(Key):
    
    @property
    def to(self):
        return [TestDataItem(i, module_name=self.module_name, 
                             list_name=self.list_name, lazy=True) for i in self.index_arg]
