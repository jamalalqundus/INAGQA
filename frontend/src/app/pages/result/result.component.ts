/**
 * Name:     result.component.ts
 * 
 * Description: The result component is the most important component next to the home page. 
 *  It initiates the request with the backend and transfers the data to the corresponding 
 *  child component depending on the result flag. The possible flags are: card, map and table.
 * 
 * 
*/

import { Component, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';
import { MatAutocompleteTrigger } from '@angular/material/autocomplete';
import { CSIService } from '../../csi.service';
import { ActivatedRoute, Router } from '@angular/router';
import { FormControl } from '@angular/forms';
import { debounceTime, tap, switchMap } from 'rxjs/operators';
import { SuggestionsService } from '../../shared/services/suggestions.service';
import { MatTabChangeEvent } from '@angular/material';

export enum ResultState {
  table, 
  map, 
  graph, 
  card,
  generator,
  barchart,
  stockchart, 
  error,
  default
}  

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class ResultComponent implements OnInit {
  @ViewChild(MatAutocompleteTrigger, {static: true}) autocompleteTrigger;

  result: any;
  tableData: any;
  mapData: any;
  graphData: any;
  cardData: any;
  generatorData: any;
  barchartData: any;
  stockchartData: any;
  errorData: any;
  spellChecked: String;
  originalSearch: String;
  isDataAvailable: boolean = false;
  resultStateEnum = ResultState;
  resultType = ResultState.default;
  selectedTab = 0;
  selectedTabObject = {
    "start":0,
    "edit":1,
    "rate":2
  }
  selectedTabObjectReversed = {
    0:"start",
    1:"edit",
    2:"rate"
  }

  //Input auto suggestion
  queryCtrl = new FormControl();
  suggestions: any;
  isLoading = false;
  errorText = {
    "no entity found in query": "Es wurde keine Entität in der Suchanfrage gefunden.",
    "more than one entity found": "Es wurden mehrere Entitäten in der Suchanfrage gefunden: ",
    "entity not found in csv": "Die Entität wurde nicht in der CSV gefunden.",
    "entity not found in api4kb": "Die Entität wurde nicht in der Wissensbasis gefunden.",
    "tuple index out of range": ""
  };
  // Dummy suggestions until sync with backend.
  searchSuggestions = ["Adidas", "Apple", "Daimler"];
  generatorMode = false;


  constructor(private CSIService: CSIService, private route: ActivatedRoute, public router: Router, private suggestionsService: SuggestionsService) {
  }

  ngOnInit() {
    this.route.params.subscribe(() => {
      this.queryCtrl.setValue(this.route.snapshot.paramMap.get("query"));
      if (this.route.snapshot.paramMap.get("tab") == "generator") {
        this.generatorMode = true;
      }
      this.initAutoComplete();
      this.getResult(this.queryCtrl.value);
    });
    this.getProperties();
  }


  openPage(company){
    this.router.navigate(['/result/start', company]);
  }

  submitQuery(query) {
    if(query) {
      this.queryCtrl.setValue(query);
      this.resultType = ResultState.default;
      if (this.generatorMode) {
        this.router.navigate(['/result/generator', query]);
      } else {
        this.router.navigate(['/result/start', query]);
      }
      this.autocompleteTrigger.closePanel();
      this.getResult(query);
    }
  }


  getProperties() {
    this.suggestionsService.getProperties().subscribe((properties) => {   
      this.result.properties.push(...JSON.parse(JSON.stringify(properties)));
      this.cardData = JSON.parse(JSON.stringify(this.result));
    }); 
  }

  initAutoComplete(): void {
    this.queryCtrl.valueChanges
      .pipe(
        debounceTime(800),
        tap(() => {
          this.suggestions = [];
          this.isLoading = true;
        }),
        switchMap(value => {
          return this.CSIService.autoSuggest(value.split(" ").splice(-1)[0]);
        })
      ).subscribe(data => {
        this.isLoading = false;
        for (var i = 0; i < data.length; i++) {
          var lastIndex = this.queryCtrl.value.lastIndexOf(" ");
          var prefix = this.queryCtrl.value.substring(0, lastIndex);
          this.suggestions.push({ label: prefix + " " + data[i].label });
        }
      });
  }

  getResult(query): void {
    this.CSIService.csi_query(query, this.generatorMode)
      .subscribe(dataSource => {
        this.result = dataSource;
        this.originalSearch = this.queryCtrl.value;
        this.spellChecked = this.result.query;

        ////////////////////////////////////////////////////
        // This "if" should only stay here until the backend 
        // implements the "generator" flag.
        ////////////////////////////////////////////////////
        if (this.generatorMode == true) {
          this.generatorData = this.result;
          this.resultType = ResultState.generator;
        }
        ////////////////////////////////////////////////////
        else if (this.result.flag == "table") {

          this.tableData = this.result.content;
          this.resultType = ResultState.table;
        }
        else if (this.result.flag == "map") {
          this.mapData = this.result.content;
          this.resultType = ResultState.map;
        }
        else if (this.result.flag == "graph") {
          this.graphData = this.result.content;
          this.resultType = ResultState.graph;
        }
        else if (this.result.flag == "card") {
          this.cardData = this.result;
          this.resultType = ResultState.card;
        } 
        else if (this.result.flag == "generator") {
          this.generatorData = this.result.content;
          this.resultType = ResultState.generator;
        }         
        else if (this.result.flag == "chart") {
          if (this.result.properties[0].datatype == "barchart"){
            this.barchartData = this.result.properties[0];
            this.resultType = ResultState.barchart;  
          }
          else if (this.result.properties[0].datatype == "stock"){
            this.stockchartData = this.result.properties[0];
            this.resultType = ResultState.stockchart;  
          }
        } else {
          this.resultType = ResultState.error;
          var errorStringArr = this.result.error.split(":");
          this.errorData = `Anfrage konnte nicht verarbeitet werden. ${this.errorText[errorStringArr[0].toLowerCase()]}`;
          
          if (errorStringArr.length > 1){
            this.errorData += errorStringArr[1];
          }
        }
        this.isDataAvailable = true;
        this.selectedTab = this.selectedTabObject[this.route.snapshot.paramMap.get("tab")];    
      });
  }

  onTabChange(event: MatTabChangeEvent) {
    this.router.navigate(['/result', this.selectedTabObjectReversed[event.index], this.route.snapshot.paramMap.get("query")]);
  }

  getTab($event) {
    this.selectedTab = this.selectedTabObject[$event];
  }
 
}

