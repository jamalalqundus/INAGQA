/**
 * Name:     data-map.component.ts
 * Author:   ssa
 * 
 * Description: Loading an openstreetmaps map based on latitude and longitude. 
 *  A list of clickable and focusable elements is rendered.
 * 
 * 
*/

import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';

declare var ol: any;

@Component({
  selector: 'app-data-map',
  templateUrl: './data-map.component.html',
  styleUrls: ['./data-map.component.css']
})
export class DataMapComponent implements OnInit {

  @Input() data:any;
  @Input() tab:any;

  displayedColumns: string[] = ['Location'];
  map: any;
  layers: any[] = [];
  highlighted: number;

  constructor(public router: Router) { }

  ngOnInit() {  
    if (this.data.length > 0){
      this.createMap(+this.data[0].lat, +this.data[0].long);
    }
    this.data = JSON.parse(JSON.stringify(this.data));
    this.data.forEach(location => {
      location.locationlabel = location.locationlabel.split(", ").join(",\n");
      this.addPoint(+location.lat, +location.long);
    });
  }

  createMap(lat: number, long: number){
    this.map = new ol.Map({
      target: 'map',
      layers: [
        new ol.layer.Tile({
          source: new ol.source.OSM()
        })
      ],
      view: new ol.View({
        center: ol.proj.fromLonLat([long, lat]),
        zoom: 3
      })
    });
  }

  addPoint(lat: number, long: number) {
    var vectorLayer = new ol.layer.Vector({
      source: new ol.source.Vector({
        features: [new ol.Feature({
          geometry: new ol.geom.Point(ol.proj.transform([long, lat], 'EPSG:4326', 'EPSG:3857')),
        })]
      }),
      style: new ol.style.Style({
        image: new ol.style.Icon({
          anchor: [0.5, 0.5],
          anchorXUnits: "fraction",
          anchorYUnits: "fraction",
          scale: 0.25,
          src: "assets/marker.svg"
        })
      })
    });
    this.layers.push(vectorLayer);
    this.map.addLayer(vectorLayer);
  }

  highlightMarker(index: number) {
    if(this.highlighted == index) {
      this.layers[index].setStyle(() => {
        return new ol.style.Style({
          image: new ol.style.Icon({
            anchor: [0.5, 0.5],
            anchorXUnits: "fraction",
            anchorYUnits: "fraction",
            scale: 0.25,
            src: "assets/marker.svg"
          })
        })
      });
      this.highlighted = undefined;
    } else {
      this.layers.forEach((layer) => {
        layer.setStyle(() => {
          return new ol.style.Style({
            image: new ol.style.Icon({
              anchor: [0.5, 0.5],
              anchorXUnits: "fraction",
              anchorYUnits: "fraction",
              scale: 0.25,
              src: "assets/marker.svg"
            })
          })
        });
      })
      this.layers[index].setStyle(() => {
        return new ol.style.Style({
          image: new ol.style.Icon({
            anchor: [0.5, 0.5],
            anchorXUnits: "fraction",
            anchorYUnits: "fraction",
            scale: 0.4,
            src: "assets/marker-highlight.svg"
          })
        })
      });
      this.highlighted = index;
    }
    this.map.getView().setCenter(ol.proj.transform([this.data[index].long, this.data[index].lat], 'EPSG:4326', 'EPSG:3857'));
    this.map.getView().setZoom(7);
  }
}

