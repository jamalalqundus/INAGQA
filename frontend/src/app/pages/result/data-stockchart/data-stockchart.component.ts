import { Component, OnInit, Input, AfterViewInit} from '@angular/core';
import { Chart, StockChart} from 'angular-highcharts';

import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-data-stockchart',
  templateUrl: './data-stockchart.component.html',
  styleUrls: ['./data-stockchart.component.css']
})
export class DataStockchartComponent implements OnInit, AfterViewInit {
  chart: Chart;
  stockChart: StockChart; 
  @Input() data: any;
  @Input() tab:any;

  constructor(private route: ActivatedRoute, public router: Router) { }
/*
  printBigNumber(bigNum: number) {
    var table = [
      { value: 1, symbol: "" },
      { value: 1E3, symbol: "T." },
      { value: 1E6, symbol: "Mio." },
      { value: 1E9, symbol: "Mrd." },
      { value: 1E12, symbol: "Bio." }
    ];
    var i: number;
    for (i = table.length - 1; i >= 0; i--) {
      if(bigNum >= table[i].value) {
        return ((bigNum / table[i].value) + ' ').replace(".", ",") + table[i].symbol;
      }
    }
  }
*/
  create_dataitems(arr:any[]){
    var i: number;
    for(i = 0; i<arr.length; i++){
      //date_to_miliseconds
      let date: Date = new Date(arr[i][0]);
      arr[i][0] = date.valueOf();
      // convert to number
      arr[i][1] = Number(arr[i][1]);

    }
    return arr;
  }

  init() {
    this.stockChart = new StockChart({
      rangeSelector: {
        selected: 1
      },

      title: {
        text: this.data.series[0].title
      },

      series: [
        {
          name: this.data.series[0].title.split(' ')[0],
          data: this.create_dataitems(this.data.series[0].data),
          type: 'spline',
          tooltip: {
            valueDecimals: 2
          }
        }
      ]
    });
  }
  ngOnInit() {
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
