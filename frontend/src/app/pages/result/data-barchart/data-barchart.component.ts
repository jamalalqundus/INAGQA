import { Component, OnInit, Input, AfterViewInit} from '@angular/core';
import { Chart} from 'angular-highcharts';

import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-data-barchart',
  templateUrl: './data-barchart.component.html',
  styleUrls: ['./data-barchart.component.css']
})
export class DataBarchartComponent implements OnInit,AfterViewInit {
  chart: Chart;
  barChart: Chart;
  @Input() data: any;
  @Input() tab:any;

  constructor(private route: ActivatedRoute, public router: Router) { }
  
  getRandomColor() {
    var length = 6;
    var chars = '0123456789ABCDEF';
    var hex = '#';
    while(length--) hex += chars[(Math.random() * 16) | 0];
    return hex;
  }
  create_dataitem(series:any []){

    for (var i in series){
      series[i] = {y:Number(series[i].y),color:this.getRandomColor()};
    }
    return series;
  }

  init() {
    this.barChart = new Chart({
      chart: {
        type: 'bar'
      },
      title: {
        text: this.data.series[0].title
      },
      yAxis: {
        visible: true
      },
      legend:{
        enabled:true
      },
      xAxis:{
        lineColor:'braun',
        categories:this.data.categories,
      },
      plotOptions:{
        series:{
          borderWidth:5,
        } as any
      },
      series: [
        {
        type:'bar',
        name: this.data.series[0].title,
        data :this.create_dataitem(this.data.series[0].data)
        }
      ]
    });
  }
  ngOnInit(): void {
    this.init();
    console.log('on init');
    /*this.chart.ref$.subscribe(chart => {
      console.log(chart);
    });*/
  }

  ngAfterViewInit() {
    console.log('after view init');
    /*this.chart.ref$.subscribe(chart => {
      console.log(chart);
    });*/
  }

  goBackToStart() {
    this.router.navigate(['/result/start', this.route.snapshot.paramMap.get("query")]);
  }

}
