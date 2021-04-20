# Theming

https://www.themeontology.org/  


## What is a Story?

Any publicly known work of fiction that can be referenced and analyzed may be a "story" in this project.
A story may take the form of a work of literature (e.g., a novel, a short story, a poem, a play), a film, a comic book, a television drama episode, a video game plot, and so on. To be admissible, a story entry must merely:

- Unambiguously identify a story from the data entered, chiefly by date and title.
- Indicate a story that's obtainable to anyone who wishes to review the themes of it.
- Come with a reasonable expectation that the previous conditions will continue to hold for a very long time.

Conventional published sources such as books and movies are nearly always acceptable.
Any determined themer (i.e., a person actively engaged in assigning themes to stories) can purchase their copy from one vendor or another.
Some examples of works that are not admissible have emerged:
Lost works (commentary may exist that elucidate themes but we have no way of reviewing the work for ourselves) are not accepted. 
Works, such those arising from student creative writing assignments, which may only be obtainable via some url online are generally not acceptable since urls frequently become broken.


## What is a Theme?

A theme is any topic of interest that is featured in a story.
A central theme is a theme that is topical throughout most of the story, either because it is featured continuously or because it pertains to the main storyline in its entirety. 
For example a "moral of the story" may be revealed only towards the end, yet is considered central because it is what most of the story was leading up to.
A peripheral theme is any theme of interest that is featured briefly.

In the notes, peripheral themes are called "minor". 
Central themes are called "major" or "choice".
Choice themes are whatever the themer may care to consider truly important in the story.

There are no strict rules for what makes a good theme to include.
There are a few rules of thumb:

- Look mostly for central themes.
- Prefer to use themes that are already defined.
- Don't waste time including uninteresting minor themes but feel free to include what interests you.
- Don't introduce themes that are specific to a particular fictional universe; generalize them instead.
- Good themes are topics that are featured significantly in various different stories.
- Look for themes that are obvious and seem uncontroversial.
- Look for themes that expose our human nature through the stories we tell.

"The desire for vengeance", "the horrors of war", "faith vs. reason", "what if I had magical powers", are examples of good themes that we find in many different stories.


## What is The Ontology?

The ontology is a hierarchical ordering of a large number of themes such that:
Theme A is "a parent" of theme B if whenever B is topical in a story, then A is also topical in that story.
Thus if theme B is found in a story, theme A is there implicitly.
Theme A is not explicitly added but many statistical analyses infer it from the presence of B to come up with interesting results.

For example, "arms race" is a child of "war", which in turn is a child of "transnational social issues". 
Whenever two large factions engage in an arms race in a story, all three of these themes become topical.

The parentage (along with the longer written description) is part of the definition of a theme.
So if the words "arms race" are interpreted in a way that does not imply "transnational social issue", then that interpretation is not in the scope for what this theme expresses.
While it is hoped that the short sequence of words representing a theme should intuitively make matters clear, this is not always the case and the real definition of a theme is both its long description as well as its parentage and the long descriptions for all the parents.


## Why?

Data from this repository can easily be incorporated into http://www.themeontology.org/. 
There it can be analyzed in various ways.
This tells us interesting things about the kind of stories we humans invent.
Theming is also a good personal way to reflect on what really goes on in the stories we enjoy.



## Practicalities

### Files

Story definitions may be entered into any file with the extension `.st.txt`. Theme definitions may be entered into any file 
with the extension `.th.txt`. The format of these files is straightforward and should be apparent from what is already there.

### Story data

Every story requires a *title*, a *date*, and a *description*. Insofar as possible, a link to the relevant Wikipedia page
is recommended as one of *references*. Most stories are unambiguously identified by their date and title. For works of
literature, the *authors* is good information to specify as well. The description is meant merely for convenience, but
may conceivably be used to distinguish between variations of a work.

- Unless there is compelling reason to distinguish between translations (or other variations) of a story, the *title* should 
be as the work is best known in English. The original title may be specified as part of the description.
- As a rule of thumb, the *date* should indicate the earliest time that the work is known to have been made available
to a broad public. 
- Two variations on a story are normally considered the same story if all themes are the same. This is often the case in
renditions of a Shakespeare play that largely adhere to the original script. If themes are different, on the other hand,
the variations are considered different and should have different story entries. This is usually the case in remakes
of films.

Every story must also be assigned a unique ID. While all text files are encoded in UTF-8, the story ID should be composed
only of normal English characters and punctuation directly mappable to ASCII. A number of conventions are apparent.

### Theme data

A theme entry should start with a theme "name". The name is also its database ID and must be unique. 
The name should be in English but may use foreign expressions and characters where it is common to do so in English writing. 
For example, the French expression "déjà vu" is commonly used in English, and has been adopted as a theme.
Insofar as is possible, this name should readily make it clear what the idea the theme expresses is.

The entry should also have a *description*. 
The description should set out necessary and sufficient conditions for when the theme applies in a story.
Relatively objective conditions are preferred as a starting point.
The more subjective an entry is, the more difficult it will be to reach a consensus about when it applies.
Exceptions, interpretations, and other subtleties may be explained either in the description or as *notes*.

*Parents* may contain any other theme that is logically implied by the present theme.
For example the theme "fatherly disappointment in a son" implies the theme "father and son".
It is recommended that the list of parents begin with a carefully chosen place to anchor the theme in the main taxonomy of the ontology.
For example if the theme concerns the relationship between two countries, it may have "international issue" as a first parent.



