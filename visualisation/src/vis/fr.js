import {ForceGraph} from "@d3/force-directed-graph"

chart = ForceGraph(miserables, {
	nodeId: d => d.id,
	nodeGroup: d => d.group,
	nodeTitle: d => `${d.id}\n${d.group}`,
	linkStrokeWidth: l => Math.sqrt(l.value),
	width,
	height: 600,
	invalidation // a promise to stop the simulation when the cell is re-run
})

import React, { Component } from 'react'
import * as d3 from 'd3'

class BarChart extends Component {
    componentDidMount() {
        this.drawChart();
    }
    drawChart() {
        const data = [12, 5, 6, 6, 3, 10];

        const svg = d3.select("body")
                    .append("svg")
                    .attr("width", 700)
                    .attr("height", 300);

        svg.selectAll("rect")
            .data(data)
            .enter()
            .append("rect")
            .attr("x", (d, i) => i * 70)
            .attr("y", (d, i) => 300 - 10 * d)
            .attr("width", 65)
            .attr("height", (d, i) => d * 10)
            .attr("fill", "green");
    }
    render() {
        return <div id={"#" + this.props.id}></div>
    }
}
export default BarChart;