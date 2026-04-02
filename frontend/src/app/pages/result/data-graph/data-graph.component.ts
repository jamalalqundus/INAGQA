/**
 * Name:     data-graph.component.ts
 * 
 * Description: This component is currently not used (legacy from cisqa19).
 * 
 * 
*/

import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { Link , Node} from './d3/models';
@Component({
  selector: 'app-data-graph',
  templateUrl: './data-graph.component.html',
  styleUrls: ['./data-graph.component.css']
})
export class DataGraphComponent implements OnInit,AfterViewInit {

  @Input()data:any;
  @Input() tab:any;
  
  nodes: Node[] = [];
  links: Link[] = [];

  constructor() {}

  ngOnInit() {
    //console.log(this.data)

    const N = 10,
    getIndex = number => number - 1;


    for (let j = 0; j <this.data.roots.length; j++) {
      var root = new Node("root"+j,this.data.roots[j].value,this.data.roots[j].entity)
      root.linkCount+=this.data.knots.length
      this.nodes.push(root);
    }

    for (let j = 0; j <this.data.knots.length; j++) {
      //Build child node
      var id="child"+j
      var node=new Node(id,this.data.knots[j].value,this.data.knots[j].entity)
      node.linkCount+=this.data.roots.length
      this.nodes.push(node);

      //Build links
      for (let k = 0; k <this.data.roots.length; k++) {
        this.links.push(new Link("root"+k, id,""));
      }
    
    }

    /*this.nodes.push(new Node(0,this.data.roots.value,this.data.roots.entity));

    for (let i = 0; i <this.data.knots.length; i++) {
      var id=i+1
      var node=new Node(id,this.data.knots[i].value,this.data.knots[i].entity)
      node.linkCount++
      this.nodes.push(node);
      this.nodes[0].linkCount++
      this.links.push(new Link(0, id,this.data.knots[i].connection));
    }*/


    /** constructing the nodes array */
    //this.nodes.push(new Node(0,this.data.roots[0].value));
    //Graph 
   /* for (let i = 0; i <this.data.roots.length; i++) {

      //Root
      
      for (let j = 0; j <this.data.roots[i].length; j++) {
        var root = new Node("root"+i+","+j,this.data.roots[i][j].value,this.data.roots[i][j].entity)
        root.linkCount+=this.data.knots[i].length
        this.nodes.push(root);
      }

      //Nodes
      for (let j = 0; j <this.data.knots[i].length; j++) {
        //Build child node
        var id="child"+i+","+j
        var node=new Node(id,this.data.knots[i][j].value,this.data.knots[i][j].entity)
        node.linkCount+=this.data.roots[i].length
        this.nodes.push(node);

        //Build links
        for (let k = 0; k <this.data.roots[i].length; k++) {
          this.links.push(new Link("root"+i+","+k, id,""));
        }
      
      }
    }*/




  }
  ngAfterViewInit(){
    
  }

}
