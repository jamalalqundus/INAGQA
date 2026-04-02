import APP_CONFIG from '../../../../../app.config';

export class Node implements d3.SimulationNodeDatum {
  // optional - defining optional implementation properties - required for relevant typing assistance
  index?: number;
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
  fx?: number | null;
  fy?: number | null;

  entityId:String;
  label:String;
  id: string;
  linkCount: number = 0;

  constructor(id,label,entityId) {
    this.id = id;
    this.label=label;
    this.entityId=entityId;
  }

 

  normal = () => {
    return Math.sqrt(this.linkCount / APP_CONFIG.N);
  }

  get r() {
    //return 200 * this.normal() + 30;
    return 3.5 * this.label.length +5 ;
  }

  get fontSize() {
    return (30 * this.normal() + 10) + 'px';
  }

  get color() {
    let index = Math.floor(APP_CONFIG.SPECTRUM.length * this.normal());
    return APP_CONFIG.SPECTRUM[index];
  }
}
