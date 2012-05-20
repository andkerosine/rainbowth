Rainbowth
=========

### What is this?
Rainbowth is a Sublime Text 2 plugin that automagically highlights matching parentheses in Lisp and Scheme source code. While the name does imply a certain sequence of colors, the palette used to paint them is entirely configurable; nonetheless, the effect is perhaps best demonstrated when viewed with a theme like [Tomorrow Night](https://github.com/chriskempson/tomorrow-theme/tree/master/textmate):

![img](http://i.imgur.com/ja50Z.png)

### Why?

It took about three hours for Racket to grow on me. I know with a fair amount of certainty that I'd like to master it, but the structure is going to take some getting used to. This plugin attempts to overcome one of the primary barriers to entry, that of not being able to tell what's related beyond the matching of a single parenthetical pair.

### Installation

Cloning the repository directly into your Packages directory is simplest.

    git clone https://github.com/andkerosine/rainbowth.git Rainbowth

### Configuration

The `palette` setting is a mapping of theme names to the list of colors to use for painting parentheses while using that theme, outermost first. When using a theme not specified, the default ROYGBIV sequence will be used.

### Roadmap

The plugin does not appear to cause any noticeable lag, but I didn't test it on any massive files. Still, there are a few places it could be improved. At present, the entire file is modified after each keyed parenthesis; ideally, I'd like to make it block-local. Implementing this feature is non-trivial due to the fact that region sets must be given unique names; identifying each block by index would break if a new block were inserted between two existing ones.

### Contributing

Comments, criticisms, and code are all eagerly welcomed.