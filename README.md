# `showast`

An IPython/Jupyter notebook plugin for visualizing abstract syntax trees.

**Added detailed info for nodes (see example below).**

## Example

See [example.ipynb](https://nbviewer.jupyter.org/github/code-gen/show_ast/blob/master/example.ipynb).

```python
import showast
```

```python
%%showast
x = self.func(1, 'test', var)
```

![example](https://i.imgur.com/KgL7ZGC.png)


## Installation
In the cloned repo directory, do
```
pip install .
```

`showast` has the following Python dependencies:
```
ipython
graphviz
```

You will also need to have [Graphviz](http://www.graphviz.org/Download..php) installed.

Use of the alternative nltk-based rendering engine requires the following packages:
```
nltk
pillow
```
When using this option, you will additionally need to have [Ghostscript](http://ghostscript.com/download/gsdnld.html) installed.

## Credits
* Name: [H. Chase Stevens](http://www.chasestevens.com)
* Twitter: [@hchasestevens](https://twitter.com/hchasestevens)
