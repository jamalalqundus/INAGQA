/**
 * Name:     data-table.component.ts
 * Author:   ssa
 * 
 * Description: Generic table with relevant information is rendered depending on the data format.
 * 
 * 
*/

import { Component, OnInit, ViewChild, Input } from '@angular/core';
import { MatPaginator, PageEvent } from '@angular/material';
import { Router } from '@angular/router';

@Component({
  selector: 'app-data-table',
  templateUrl: './data-table.component.html',
  styleUrls: ['./data-table.component.css']
})

export class DataTableComponent implements OnInit {
  @Input() data: any;
  @Input() tab:any;
  
  @ViewChild(MatPaginator, { static: true }) paginator: MatPaginator;
  displayedColumns: any[] = [];
  displayedColumnsTypes: any[] = [];
  pageEvent: PageEvent;
  pageSizeOptions: number[] = [1, 5, 10, 20];
  pageSize: number = this.pageSizeOptions[1];
  firstIndex: number = 0;
  lastIndex: number = this.pageSize;


  constructor(public router: Router) { }

  ngOnInit(): void {
    this.loadTable();
  }

  loadTable(){
    this.data.headers.forEach(header => {
      this.displayedColumns.push(header.label);
    });
    this.data.headers.forEach(header => {
      this.displayedColumnsTypes.push(header.type);
    });
  }

  printDate(dateString: string): string {
    var dateObject = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return dateObject.toLocaleDateString('de-DE', options);
  }

  setPagination(first: number, last: number){
    this.firstIndex = first;
    this.lastIndex = last;
  }
}