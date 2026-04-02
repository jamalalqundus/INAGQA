/**
 * Name:     data-generator.component.ts
 * 
 * Description: This component displays text generated from multiple questions.
 * 
 * 
*/

import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import { CSIService } from '../../../csi.service';

@Component({
  selector: 'app-data-generator',
  templateUrl: './data-generator.component.html',
  styleUrls: ['./data-generator.component.css']
})
export class DataGeneratorComponent implements OnInit {
  @Input() data: any;
  outputGroup: FormGroup;
  outputString = ""; 


  constructor(public router: Router, private csiService: CSIService){}

  ngOnInit() {
    this.outputString = "Das ist ein Beispieltext: " + this.data.entity;
    this.outputGroup = new FormGroup({
      outputData: new FormControl(this.outputString)
   });
  }

  onSubmit(){
    window.open(this.csiService.getText(this.outputGroup.value.outputData), '_blank');
  }

}
