/**
 * Name:     app.component.ts
 * 
 * Description: Root component containing all other components.
 * 
 * 
*/

import { Component, ViewChild, OnInit } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
import { SuggestionsService } from './shared/services/suggestions.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'frontend';
  @ViewChild('drawer', {static: true}) drawer: MatSidenav;
  count: number = 0;

  constructor(private suggestionsService: SuggestionsService) {}

  ngOnInit() {
    this.suggestionsService.setDrawer(this.drawer);
    this.getBadgeCount();
  }

  toggleDrawer() {
    this.suggestionsService.toggleDrawer();
  }

  getBadgeCount() {
    this.suggestionsService.getNumberOfNewSuggestions().subscribe((number) => {
      this.count = number;
    });
  }
}
