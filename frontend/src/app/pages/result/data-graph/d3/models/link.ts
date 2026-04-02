import { Node } from '.';

export class Link implements d3.SimulationLinkDatum<Node> {
  // optional - defining optional implementation properties - required for relevant typing assistance
  index?: number;
  label:String;

  // must - defining enforced implementation properties
  source: Node | string | number;
  target: Node | string | number;

  constructor(source, target,label) {
    this.source = source;
    this.target = target;
    this.label=label;
  }
}
