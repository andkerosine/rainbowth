import sublime, sublime_plugin

class Rainbowth(sublime_plugin.EventListener):
  def __init__(self):
    settings = sublime.load_settings('rainbowth.sublime-settings')
    self.style = settings.get('style') == 'outline' and 32 or 0
    self.sources = settings.get('sources')

  def is_lispy(self):
    file_scope = self.view.scope_name(0)
    return file_scope.split('.')[1].split(' ')[0] in ['lisp', 'scheme']

  def on_modified(self, view):
    key = view.substr(view.sel()[0].begin() - 1)
    if key not in '()':
      return

    try:
      self.lispy
    except AttributeError:
      self.view = view
      self.lispy = self.is_lispy()
    if not self.lispy:
      return

    start, end = [view.sel()[0].begin()] * 2

    while start > 0:
      start -= 1
      if view.substr(sublime.Region(start, start + 2)) == "\n\n":
        break
    while end < view.size() - 1:
      end += 1
      if view.substr(sublime.Region(end, end + 2)) == "\n\n":
        break

    if start > 0:
      start += 2
    if end >= view.size():
      end -= 1

    level, parens = 0, [[] for x in range(len(self.sources))]
    for i in range(start, end + 1):
      char = view.substr(i)
      if char == '(':
        parens[level].append(sublime.Region(i, i + 1))
        level += 1
      elif char == ')':
        level -= 1
        parens[level].append(sublime.Region(i, i + 1))

    for i in range(len(parens)):
      view.erase_regions('rainbowth_%d' % i)

    for i, regions in enumerate([p for p in parens if p]):
      view.add_regions('rainbowth_%d' % i, regions, self.sources[i], self.style)