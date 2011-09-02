App Size Conventions
====================

If your app is aimed at the general web user population, **your app should render 
correctly in a <DIV> that is** *maximum* **768 pixels wide!**

Indivo UI assumes that the user's minimum browser size is 1024 pixels wide by 768 
pixels high. Taking Indivo UI's interface elements into account, this leaves 768 
pixels of width for your app content.

**The safe assumption is that your app content has 768px of width, but no more**

Many users will have screen resolutions that make this the maximum width of app
content they will be able to display. If your app exceeds 768 pixels wide by
default, the majority of the general web user's browsers will side-scroll, which is
poor user experience and to be avoided. For users with higher resolution
screens, the Indivo UI will expand and provide your app with more pixels of
width that you can take advantage of using a "liquid" layout in your app, but a
wider screen cannot be assumed by default for the general web user population.

As for length, there are less strict criteria, since the length of the
app_content_pane will expand to fit longer content and we assume that users will
scroll vertically. Be aware that empirical browser size research shows that for
90% of users the bottom edge of their browser window is at approximately 500
pixels and for 80% of users the bottom edge is around 560 pixels. To provide a
good experience for your users it's important to keep key data and interface
elements "above the fold" e.g. above 500 to 560 pixels.

