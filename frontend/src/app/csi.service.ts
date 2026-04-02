/**
 * Name:     csi.service.ts
 * Author:   FU students & ssa
 * 
 * Description: Service handling API calls with the backend.
 * 
 * 
*/

import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of ,empty} from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { MessageService } from './message.service';
import { ConfigService } from './config.service';


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'}),
  withCredentials:true
};

@Injectable({ providedIn: 'root' })
export class CSIService {
  private url = this.configService.getKey("API_URL");  // URL to web api
  
  constructor(
    private http: HttpClient,
    private messageService: MessageService,
    private configService: ConfigService) { }

    csi_query (question, generatorMode): Observable<any> {
      return this.http.get<any>(this.url + this.configService.getKey("QUERY_ENDPOINT") +"?query="+question+"&generatorMode="+generatorMode, httpOptions)  
      .pipe(
        tap(_ => this.log('fetched results')),
        catchError(this.handleError<any>('QUERY_ENDPOINT'))
      );
  }
  
  autoSuggest (query): Observable<any> {
    if(query=="" || query==" "){
      return empty();
    } else {
      return this.http.get<any>(this.url + this.configService.getKey("AUTOSUGGEST_ENDPOINT")+"?query="+query, httpOptions)
        .pipe(
          tap(_ => this.log('fetched results')),
          catchError(this.handleError<any>('AUTOSUGGEST_ENDPOINT'))
        );
    }
  }
  pickattributes (id): Observable<any> {
    return this.http.get<any>(this.url + this.configService.getKey("ATTRIBUTES_ENDPOINT")+"?id="+id, httpOptions)
      .pipe(
        tap(_ => this.log('fetched results')),
        catchError(this.handleError<any>('ATTRIBUTES_ENDPOINT'))
      );
  }

  submitProperties(data): Observable<any> {
    return  this.http.put<any>(this.url + this.configService.getKey("SUBMITATTRIBUTES_ENDPOINT"),JSON.stringify(data), httpOptions)
    .pipe(
      tap(_ => this.log('fetched results')),
      catchError(this.handleError<any>('SUBMITATTRIBUTES_ENDPOINT'))
    );
  }

  pickConstraints (id): Observable<any> {
    return this.http.get<any>(this.url + this.configService.getKey("CONSTRAINTS_ENDPOINT")+"?id="+id, httpOptions)
      .pipe(
        tap(_ => this.log('fetched results')),
        catchError(this.handleError<any>('CONSTRAINTS_ENDPOINT'))
      );
  }

  suggestQuestion (count): Observable<any> {
    return this.http.get<any>(this.url + this.configService.getKey("SUGGEST_QUESTION_ENDPOINT")+"?count="+count, httpOptions)
      .pipe(
        tap(_ => this.log('fetched results')),
        catchError(this.handleError<any>('SUGGEST_QUESTION_ENDPOINT'))
      );
  }

  getText (text): string {
    return this.url + this.configService.getKey("GET_TEXT_ENDPOINT")+"?text="+text;
  }

  
  /**
   * Handle Http operation that failed.
   * Let the app continue.
   * @param operation - name of the operation that failed
   */
  private handleError<T> (operation = 'operation') {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      // console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      this.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(error.error as T);
    };
  }

  /** Log a ReportService message with the MessageService */
  private log(message: string) {
    this.messageService.add(`CSIService: ${message}`);
  }
}


/*
Copyright Google LLC. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/