
// Load the items from the JINJA template
var items = {{result_list|tojson}};


width = 700;
height = 200;
radius = 20;

// Start the force directed layout
var force = d3.layout.force()
    .charge(-50)
    .chargeDistance(100)
    .gravity(.25)
    .linkDistance(0)
    .size([width, height]);


var svg = d3.select("#viz")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

// Draw a background rectangle
svg.append("rect")
    .attr("width", "100%")
    .attr("height", "100%")
    .attr("fill", "pink");


graph = {};
graph["nodes"] = [];
graph["links"] = [];

for(idx in items) {
    var name = items[idx][0];
    var distance = items[idx][1];
    var time = items[idx][2];

    // Original x and y values
    var ox = time*(width-2*radius) + radius;
    var oy = height-radius-distance*(height-2*radius);

    node = {
        "name":items[idx][0],
        "distance":items[idx][1],
        "time":items[idx][2],
        "ox":ox,
        "oy":oy,
        "idx":idx,
        "startAngle":0,
        "endAngle":0
    };
    
    graph["nodes"].push(node);
};


force
    .nodes(graph.nodes)
    .links(graph.links)
    .start();

var link = svg.selectAll(".link")
    .data(graph.links)
    .enter().append("line")
    .attr("class", "link")
    .style("stroke-width", function(d) { return Math.sqrt(d.value); });

var node = svg.selectAll("g")
    .data(graph.nodes)
    .enter().append("g")
    .attr("class", "node")
    .attr("transform", function(d) {
        return "translate(" + d.ox + "," + d.oy + ")";})
    .call(force.drag);


node.append("circle")
    .attr("r", radius)
    .attr("cx", 0)
    .attr("cy", 0)
    .attr("fill", "white")
    .style("fill-opacity", .25)

// Create the text for each block 
node.append("text")
    .attr("text-anchor", "middle")
    .text(function(d){return d.name})

force.on("tick", function(e) {

    node.attr("transform", function(d) {
        return "translate(" + d.ox + "," + d.y + ")";
    });

});


/*
force.on("tick", function(e) {
    console.log(e);
    node.attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
    });

});
*/

/*
force.on("tick", function() {
    //console.log("HERE");
    var textOffset = 14;
    var prev;
    node.each(function(d, i) {
        if(i > 0) {
            var thisbb = this.getBoundingClientRect(),
                prevbb = prev.getBoundingClientRect();
            // move if they overlap
            if(!(thisbb.right < prevbb.left || 
                 thisbb.left > prevbb.right || 
                 thisbb.bottom < prevbb.top || 
                 thisbb.top > prevbb.bottom)) {
                var ctx = thisbb.left + (thisbb.right - thisbb.left)/2,
                    cty = thisbb.top + (thisbb.bottom - thisbb.top)/2,
                    cpx = prevbb.left + (prevbb.right - prevbb.left)/2,
                    cpy = prevbb.top + (prevbb.bottom - prevbb.top)/2,
                    off = Math.sqrt(Math.pow(ctx - cpx, 2) +
                                    Math.pow(cty - cpy, 2))/2;
                d3.select(this).attr("transform",
                                     "translate("
                                     + Math.cos(((d.startAngle + d.endAngle - Math.PI) / 2)) *
                                     (radius + textOffset + off) + "," +
                                     Math.sin((d.startAngle + d.endAngle - Math.PI) / 2) *
                                     (radius + textOffset + off) + ")");
            }
        }
        prev = this;
    });
    
    
});
*/

/*
var node = svg.selectAll(".node")
    .data(graph.nodes)
    .enter().append("circle")
    .attr("class", "node")
    .attr("r", 20)
    .attr("cx", function(d) { return d.ox; })
    .attr("cy", function(d) { return d.oy; })
    .style("fill", function(d) { return "red"; })
    .style("fill-opacity", .5)
    .call(force.drag)
*/
//    .enter().append("circle")




/*
var node = svg.selectAll(".node")
    .data(graph.nodes)
    .enter().append("g")
    .attr("class", "node")
    .call(force.drag);

node
    .enter().append("circle")
    .attr("r", 20)
    .attr("cx", function(d) { return d.ox; })
    .attr("cy", function(d) { return d.oy; })
    .style("fill", function(d) { return "red"; })
    .style("fill-opacity", .5)
*/
/*
node
    .attr("dx", 12)
    .attr("dy", ".35em")
    .text(function(d) { return d.name });
*/
   
//node.append("title")
//    .text(function(d) { return "FOO!"; });

/*
force.on("tick", function() {
    /*
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });
    
    //node.attr("cx", function(d) { return d.x; });
    //    .attr("cy", function(d) { return d.y; });

    node.attr("cy", function(d) {

        // Fix end nodes
        if(d.idx==0)
            return height/2;
        if(d.idx==(node[0].length-1))
            return height/2;

        return d.y;
    });

    //console.log(node[0][0]);
    */
    
/*
    node.attr("transform", function(d) {
            console.log(d);
        return "translate(" + d.x + "," + d.y + ")"; });
  
});
*/

/*
function mousedown() {
  nodes.forEach(function(o, i) {
    o.x += (Math.random() - .5) * 40;
    o.y += (Math.random() - .5) * 40;
  });
  force.resume();
}



var groups = svg.selectAll("g")
    .data(items)
    .enter()
    .append("g");


groups.attr("transform", function(d, i) {
    var name = d[0];
    var distance = d[1];
    var time = d[2];

	  var x = time*(width-2*radius) + radius;
    var y = height-radius-distance*(height-2*radius);

    return "translate(" + [x,y] + ")";
});
*/
/*

var circles = groups.append("circle")
    .attr({
      cx: function(d,i){
        return 0;
      },
      cy: function(d,i){
        return 0;
      },
      r: 18,
      fill: "#BADBDA",
      stroke: "#2F3550",
      "stroke-width": 2.4192
    });

var label = groups.append("text")
    .text(function(d){
      return d[0];
    })
    .attr({
      "alignment-baseline": "middle",
      "text-anchor": "middle"
    });
*/
