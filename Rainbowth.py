import sublime, sublime_plugin, re, pickle, os

class Rainbowth(sublime_plugin.EventListener):
  def update_colors(self, view):
    base_dir = sublime.packages_path()
    scheme_path = base_dir[:-8] + view.settings().get('color_scheme')
    scheme_name = scheme_path.split('/')[-1].split('.')[0]

    try:
      cache = pickle.load(open(base_dir + '/Rainbowth/Rainbowth.cache', 'r'))
    except:
      cache = {}

    settings = sublime.load_settings('Rainbowth.sublime-settings')
    palettes = settings.get('palettes')
    self.colors = palettes.get(scheme_name, palettes['default'])
    if self.colors == cache.get(scheme_name, None):
      return

    scheme_file = open(scheme_path, 'r')
    scheme_xml = scheme_file.read().decode('utf-8')

    bg = re.search('background.+?g>(.+?)<', scheme_xml, re.DOTALL).group(1)
    bg = '#%06x' % max(1, (int(bg[1:], 16) - 1))
    fragment = '<dict><key>scope</key><string>rainbowth%d</string><key>settings</key><dict><key>background</key><string>' + bg + '</string><key>foreground</key><string>%s</string></dict></dict>'
    scheme_xml = re.sub('\t+<!-- rainbowth -->.+\n', '', scheme_xml)

    rainbowth = '\t<!-- rainbowth -->'
    for i, c in enumerate(self.colors):
      rainbowth += fragment % (i, c)

    scheme_xml = re.sub('</array>', rainbowth + '<!---->\n\t</array>', scheme_xml)
    scheme_file = open(scheme_path, 'w')
    scheme_file.write(scheme_xml.encode('utf-8'))
    scheme_file.close()
    cache[scheme_name] = self.colors
    pickle.dump(cache, open(base_dir + '/Rainbowth/Rainbowth.cache', 'w'))

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

    source = view.substr(sublime.Region(0, view.size()))
    src_len = len(source)
    try:
      block_end = source.index('\n\n(', view.sel()[0].begin())
    except ValueError:
      block_end = src_len
    try:
      block_start = block_end - source[::-1][src_len - block_end:].index('(\n\n') - 1
    except ValueError:
      block_start = 0

    parens = [(sublime.Region(i + block_start, i + block_start + 1), c)
      for i, c in enumerate(source[block_start:block_end]) if c in '()']

    level, depths = 0, [[sublime.Region(-1, 0)] for i in xrange(len(self.colors))]
    for p in parens:
      level += p[1] == ')' and -1 or 0
      depths[level % len(self.colors)].append(p[0])
      level += p[1] == '(' and 1 or 0

    for i, regions in enumerate(depths):
      view.erase_regions('rainbowth%d' % i)
      view.add_regions('rainbowth%d' % i, regions, 'rainbowth%d' % i)