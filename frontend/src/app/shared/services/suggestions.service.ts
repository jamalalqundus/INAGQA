/**
 * Name:     suggestions.service.ts
 * 
 * Description: The suggestions service handles suggestions from 
 *  wikidata using the server sent events principle. 
 *  The service is outsourced from the csi service due to having multiple helper functions.
 * 
 * 
*/

import { Injectable, OnDestroy } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of, from, Subject } from 'rxjs';

import { ConfigService } from '../../config.service'

const httpOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'}),
    withCredentials:true
};
  
@Injectable()
export class SuggestionsService implements OnDestroy {      
    private drawer: MatSidenav;
    private receivedQueries = [];
    private data = new Subject<any>();
    private newCount = new Subject<number>();
    properties = new Subject<any>();
    source: any;

    constructor(
        private http: HttpClient,
        private configService: ConfigService) { }
    
    setDrawer(drawer: MatSidenav) {
        this.drawer = drawer;
    }

    toggleDrawer(): void {
        this.drawer.toggle();
        this.newCount.next(0);
    }

    openDrawer(): void {
        this.drawer.open();
        this.newCount.next(0);
    }

    closeDrawer(): void {
        this.drawer.close();
    }

    suggestAnswer(): void {
        this.source = new EventSource(this.configService.getKey("API_URL") + this.configService.getKey("SUGGEST_ANSWER_ENDPOINT"), httpOptions);
        this.source.onmessage = ((event) => {
            let jsonData = JSON.parse(event.data);
            jsonData = jsonData.filter(query => {
                if(!this.receivedQueries.includes(query.query)){
                    this.receivedQueries.push(query.query);
                    return query;
                }
            });
            if(jsonData.length){
                this.data.next(jsonData);
                this.newCount.next(jsonData.length);
            }
        });
    }    
    
    getData(): Observable<any>{
        return this.data;
    }

    getNumberOfNewSuggestions(): Observable<number> {
        return this.newCount;
    }

    addProperties(properties): void {
        this.properties.next(properties);
    }

    getProperties(): Observable<any> {
        return this.properties;
    }

    ngOnDestroy() {
        this.source.close();
    }
}
