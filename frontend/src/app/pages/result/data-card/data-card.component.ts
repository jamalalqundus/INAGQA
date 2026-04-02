/**
 * Name:     data-card.component.ts
 * Author:   ssa
 * 
 * Description: This component displays basic information about a company (data from DBpedia).
 * 
 * 
*/

import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { trigger, style, transition, animate } from '@angular/animations'

import { CSIService } from '../../../csi.service';

@Component({
  selector: 'app-data-card',
  templateUrl: './data-card.component.html',
  styleUrls: ['./data-card.component.css'],
  animations: [
    trigger('attributes', [
      transition(':enter', [
        style({ transform: 'scale(0.8)', opacity: 0 }),  // initial
        animate('0.5s cubic-bezier(.5, -0.6, 0.2, 1.5)', 
          style({ transform: 'scale(1)', opacity: 1 }))  // final
      ]),
      transition(':leave', [
        style({ transform: 'scale(1)', opacity: 1, height: '*' }),
        animate('0.5s cubic-bezier(.5, -0.6, 0.2, 1.5)', 
         style({ 
           transform: 'scale(0.8)', opacity: 0, 
           height: '0px', margin: '0px' 
         })) 
      ])      
    ]) 
  ]
})
export class DataCardComponent implements OnInit {
  private _data: any;
    
  @Input() set data(value: any) {
    this._data = value;
    this.resetForms();
  }
  
  get data(): any {
    return this._data;
  }

  @Input() tab:any;
  @Output() tabChange = new EventEmitter<string>();

  max = 5;
  min = 0;
  step = 1;
  thumbLabel = true;
  value: any;
  labelForm: FormGroup;
  valueForm: FormGroup;
  editIndex = 0; 
  attributeNamingDE = {
    "description":"Beschreibung",
    "foundedBy":"Gründer",
    "foundationPlace":"Gründungsort",
    "keyPerson":"CEO",
    "industry":"Branche",
    "product":"Produkt",
    "locationCity":"Ort",
    "assets":"Aktiva",
    "equity":"Eigenkapital",
    "revenue":"Umsatz",
    "netIncome":"Nettogewinn",
    "0_Nettoeinkommen":"Einkommen"
  }

  strip_label(label){
    label = label.replace(/\d_/g, "");
    return label;
  }
  
  constructor(private route: ActivatedRoute, public router: Router, private csiService: CSIService){}

  ngOnInit() {
    this.value = new Array(this.data.properties.length + 1).fill(0);
    this.editIndex = this.data.properties.length + 1;
    this.resetForms();
  }

  resetForms(){
    var group = {}
    this.data.properties.forEach(element => {
      group[element.property] = new FormControl(element.property);
    });
    this.labelForm = new FormGroup(group);
    var group = {}
    this.data.properties.forEach(element => {
      group[element.property] = new FormControl(element.value);
    });
    this.valueForm = new FormGroup(group);
  }

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

  calculateRating(){
    this.value[this.data.properties.length] = Math.floor(this.value.slice(0, this.value.length - 1).reduce((a,b) => (a+b)) / (this.value.length-1));
  }

  onSubmit(){
    for (var key in this.labelForm.value){
      var field = this.data.properties.find(element => element.property === key);
      if(!field) {
        this.data.properties.push({
          "property":this.labelForm.value[key],
          "type":"added",
          "value":this.valueForm.value[key]
        })
      } else if((this.valueForm.value[key] != field.value) || (this.labelForm.value[key] != key)) {
        field.value = this.valueForm.value[key];
        field.type = "added";  
        field.property = this.labelForm.value[key];
      } 
    }
    this.resetForms();
    this.csiService.submitProperties(this.data)
    .subscribe(data => {
      // this.data = data;
      this.goBackToStart();
    });
  }

  addField(){
    this.labelForm.addControl('Beschreibung-' + this.editIndex, new FormControl('Beschreibung-' + this.editIndex));
    this.valueForm.addControl('Beschreibung-' + this.editIndex, new FormControl(''));
    this.data.properties.push({
      "property":'Beschreibung-' + this.editIndex,
      "type":"added",
      "value":""
    })
    this.editIndex++;
  }

  deleteField(element, index) {
    this.labelForm.removeControl(element.property);
    this.valueForm.removeControl(element.property);
    this.data.properties.splice(index, 1);
  }

  goBackToStart() {
    this.router.navigate(['/result/start', this.route.snapshot.paramMap.get("query")]);
    this.tabChange.emit('start');
  }
}
