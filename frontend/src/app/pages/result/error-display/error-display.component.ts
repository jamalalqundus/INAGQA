/**
 * Name:     error-display.component.ts
 * 
 * Description: If no result is given, this component displays the error message.
 * 
 * 
*/

import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-error-display',
  templateUrl: './error-display.component.html',
  styleUrls: ['./error-display.component.css']
})
export class ErrorComponent implements OnInit {

  @Input()
  data:any;
  error:string;
  @Input() tab:any;

  constructor() {}

  ngOnInit() {
    this.error = this.data
  }

}
