import sublime, sublime_plugin, re

class Rainbowth(sublime_plugin.EventListener):
  def update_colors(self, view):
    base_dir = sublime.packages_path()[:-8]
    theme_path = base_dir + view.settings().get('color_scheme')
    theme_name = theme_path.split('/')[-1].split('.')[0]
    theme_file = open(theme_path, 'r')
    theme = theme_file.read().decode('utf-8')
    theme_file.close()

    settings = sublime.load_settings('Rainbowth.sublime-settings')
    palette = settings.get('palette')
    self.colors = palette.get(theme_name, palette['default'])

    bg = re.search('background.+?g>(.+?)<', theme, re.DOTALL).group(1)
    bg = '#%06x' % max(1, (int(bg[1:], 16) - 1))
    fragment = '<dict><key>scope</key><string>rainbowth%d</string><key>settings</key><dict><key>background</key><string>%s</string><key>foreground</key><string>%s</string></dict></dict>'
    theme = re.sub('\t+<!-- rainbowth -->.+\n', '', theme)

    rainbowth = '\t<!-- rainbowth -->'
    for i, c in enumerate(self.colors):
      rainbowth += fragment % (i, bg, c)

    theme = re.sub('</array>', rainbowth + '<!-- pot of gold -->\n\t</array>', theme)
    theme_file = open(theme_path, 'w')
    theme_file.write(theme.encode('utf-8'))
    theme_file.close()

  def on_load(self, view):
    file_scope = view.scope_name(0)
    self.lispy = file_scope.split('.')[1].split(' ')[0] in ['lisp', 'scheme']
    if self.lispy:
      self.update_colors(view)
      self.on_modified(view, True)

  def on_modified(self, view, load = False):
    if not self.lispy:
      return

    key = view.substr(view.sel()[0].begin() - 1)
    if key not in '()' and not load:
      return

    level, parens = 0, [[] for x in range(16)]
    for i in range(view.size()):
      char = view.substr(i)
      if char == '(':
        parens[level].append(sublime.Region(i, i + 1))
        level += 1
      elif char == ')':
        level -= 1
        parens[level].append(sublime.Region(i, i + 1))

    for i in range(len(parens)):
      view.erase_regions('rainbowth%d' % i)

    for i, regions in enumerate([p for p in parens if p]):
      view.add_regions('rainbowth%d' % i, regions, 'rainbowth%d' % i)