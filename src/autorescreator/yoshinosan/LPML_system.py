
class LPML_system:
  def interpret(self,tree, tools):
      if isinstance(tree, str):
          return []
      if tree is None:
          return []
      outputs = []
      for element in tree:
          if not isinstance(element, dict):
              continue
          if element['tag'] in tools:
              output = tools[element['tag']](element)
              output['attributes']['tool'] = element['tag']
              outputs += [output, '\n\n']
              continue
          outputs += interpret(element['content'], tools)
      return outputs
