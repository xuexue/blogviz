graph = {}
graph.render() {
  // figure out faceting
  // ... coord
  // ... make global scale

  // create cells for each facet

  layers.forEach(function(l) {
    facet.forEach(function(e) {
      // get the right cell
      layer.render(cell, ... )
    });
  });
}


layer = {}
layer.render(obj, scales) {
}
