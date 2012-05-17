Rainbowth
=========

### What is this?
Rainbowth is a Sublime Text 2 plugin that automagically highlights matching parentheses in Lisp and Scheme source code. While the name does imply a certain sequence of colors, Rainbowth will use your active theme to paint the parens; nonetheless, the effect is perhaps best demonstrated when viewed with a theme like [Tomorrow Night](https://github.com/chriskempson/tomorrow-theme/tree/master/textmate):

![img](http://i.imgur.com/oYWUj.png)

### Why?

It took about three hours for Racket to grow on me. I know with a fair amount of certainty that I'd like to master it, but the structure is going to take some getting used to. This plugin attempts to overcome one of the primary barriers to entry, that of not being able to tell what's related beyond the matching of a single parenthetical pair.

### How does it work?

Rainbowth is currently a bit limited in its ability to detect logical blocks of code. After each keyed parenthesis, it will look before and after the cursor until it finds two newlines on either side; these demarcate the section of code to be highlighted as a single entity. In short, this means that a blank line must be inserted between each block. This seems to be the community's preferred structure anyhow, but it's something to keep in mind in the event of strange results.

### Installation

Cloning the repository directly into your Packages directory is simplest.

    git clone https://github.com/andkerosine/rainbowth.git rainbowth
    
### Configuration

The `style` setting takes one of two values: "outline", demonstrated in the above image, or "block":

![img](http://i.imgur.com/xEMI2.png)

Neither is particularly pleasant, but the API doesn't appear to support changing the foreground color of a region at this time. Which style looks better will largely depend on how strongly your selected source colors contrast with each other. On that note, the `sources` setting is, obviously enough, a list of selectors from your theme to use in determining which color to paint each level of parentheses, outermost first.

### Roadmap

The plugin does not appear to cause any noticeable lag, but I didn't test it on any massive files. Still, there are a few places it could be improved. At present, only the currently active block gets colorized; this is sufficient, given the overall intent of the plugin, but maintaining highlighting throughout would be more aesthetically pleasing. Implementing this feature is non-trivial due to the fact that region sets must be given unique names; identifying each block by index would break if a new block were inserted between two existing ones.

### Contributing

Comments, criticisms, and code are all eagerly welcomed.