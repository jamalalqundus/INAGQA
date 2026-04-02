/**
 * Name:     home.component.ts
 * 
 * Description: Start page with animated questions to show the user 
 *  what data is available in the knowledge base. 
 * 
 * 
*/

import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { FormControl } from '@angular/forms';
import { debounceTime, tap, switchMap } from 'rxjs/operators';
import { CSIService } from '../../csi.service';
import { trigger, style, transition, animate } from '@angular/animations'

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  animations: [
    trigger('items', [
      transition(':enter', [
        style({ transform: 'scale(0.5)', opacity: 0 }),  // initial
        animate('1s cubic-bezier(.8, -0.6, 0.2, 1.5)', 
          style({ transform: 'scale(1)', opacity: 1 }))  // final
      ]),
      transition(':leave', [
        style({ transform: 'scale(1)', opacity: 1, height: '*' }),
        animate('1s cubic-bezier(.8, -0.6, 0.2, 1.5)', 
         style({ 
           transform: 'scale(0.5)', opacity: 0, 
           height: '0px', margin: '0px' 
         })) 
      ])      
    ]) 
  ]
})
export class HomeComponent  implements OnInit, OnDestroy {
 
  title = 'Home Page';
  queryCtrl = new FormControl();
  suggestions: any;
  isLoading = false;
  questions: any[];
  interval: any;
  generatorMode = false;


  constructor(private CSIService: CSIService,public router: Router) {}

  submitQuery(query) {
    if(this.generatorMode) {
      this.router.navigate(['result/generator', query]);
    } else if (query) {

      this.router.navigate(['/result/start', query]);
    }
  }

  ngOnInit() {
    this.queryCtrl.valueChanges
      .pipe(debounceTime(800), tap(() => {
          this.suggestions = [];
          this.isLoading = true;
        }),
        switchMap(value => { 
          return this.CSIService.autoSuggest(value.split(" ").splice(-1)[0])
        })
      ).subscribe(data => {
        this.isLoading=false;
        for (var i=0;i<data.length;i++) {
          var lastIndex = this.queryCtrl.value.lastIndexOf(" ");
          var prefix = this.queryCtrl.value.substring(0, lastIndex);
          this.suggestions.push({label:prefix+" "+data[i].label})
        }
      });
      this.CSIService.suggestQuestion(5)
      .subscribe(data => {
        this.questions = data.questions;
      });
      this.interval = setInterval(()=> { 
        this.questions.splice(0, 1); 
        this.CSIService.suggestQuestion(1)
        .subscribe(data => {
          this.questions.push(data.questions[0]);
        });
      }, 7 * 1000);
  }

  ngOnDestroy(){
    clearInterval(this.interval);
  }
}
