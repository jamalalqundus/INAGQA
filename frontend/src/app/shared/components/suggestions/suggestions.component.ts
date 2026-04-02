/**
 * Name:     suggestions.component.ts
 * Author:   ssa
 * 
 * Description: This component is the side panel with the suggestions from wikidata, 
 *  if no relevant information is available in API4KB. 
 *  It can be viewed from both the start and result page and is therefore a shared component. 
 * 
 * 
*/

import { Component, OnInit, NgZone } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Router } from '@angular/router';

import { SuggestionsService } from '../../services/suggestions.service';

@Component({
    selector: 'app-suggestions',
    templateUrl: './suggestions.component.html',
    styleUrls: ['./suggestions.component.css']
})
export class SuggestionsComponent implements OnInit{
  panelOpenState: boolean = false;
  data: any = [];

  constructor(private http: HttpClient, 
              private suggestionsService: SuggestionsService,
              private snackBar: MatSnackBar,
              private zone: NgZone,
              private route: ActivatedRoute, 
              public router: Router) {}

  ngOnInit() {
    this.suggestionsService.suggestAnswer();
    this.suggestionsService.getData().subscribe((data) => {
      this.data.push(...data);
      this.zone.run(() => {
        let snackBarRef = this.snackBar.open(`Es liegen ${data.length} neue Infomationen zu Ihren Fragen vor.`, "Anzeigen", {
          duration: 10000,
          verticalPosition: 'top'
        });
        snackBarRef.onAction().subscribe(() => this.suggestionsService.openDrawer());
      });
    });
  }

  closeDrawer() {
    this.suggestionsService.closeDrawer();
  }

  addToProperties(properties) {
    this.suggestionsService.addProperties(properties);
  }

  navigateToQuery(query){
    this.router.navigate(['/result/edit', query.query]);
  }
}
  