/**
 * Name:     app.module.ts
 * 
 * Description: Angular modules are containers for a cohesive block 
 *  of code dedicated to an application domain or a closely related set of capabilities.
 *  To use the modules in the application they have to be imported here.
 * 
 * 
*/

// Angular standards 
import { MatToolbarModule, MatSidenavModule, MatListModule, MatDialogModule,
  MatButtonModule, MatIconModule, MatInputModule, MatTableModule, MatPaginatorModule, MatFormFieldModule, MatAutocompleteModule,MatSelectModule,MatExpansionModule,MatBadgeModule,MatTabsModule,MatSliderModule,MatButtonToggleModule,MatSnackBarModule, MatChipsModule, MatSlideToggleModule} from "@angular/material";
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AgmCoreModule } from '@agm/core';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import {CdkTableModule} from '@angular/cdk/table'; 
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FlexLayoutModule } from '@angular/flex-layout';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { ChartModule, HIGHCHARTS_MODULES } from 'angular-highcharts';
import more from 'highcharts/highcharts-more.src';
import exporting from 'highcharts/modules/exporting.src';


//Components
import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';
import { ResultComponent } from './pages/result/result.component';
import { SuggestionsComponent } from './shared/components/suggestions/suggestions.component';
import { DataTableComponent } from './pages/result/data-table/data-table.component';
import { DataMapComponent } from './pages/result/data-map/data-map.component';
import { DataGraphComponent } from './pages/result/data-graph/data-graph.component';
import { ErrorComponent } from './pages/result/error-display/error-display.component';
import { D3Service, D3_DIRECTIVES } from './pages/result/data-graph/d3';
import { GraphComponent } from './pages/result/data-graph/visuals/graph/graph.component';
import { SHARED_VISUALS } from './pages/result/data-graph/visuals/shared';
import { DataCardComponent } from './pages/result/data-card/data-card.component';
import { DataGeneratorComponent } from './pages/result/data-generator/data-generator.component';

// Services
import { ConfigModule, ConfigService } from './config.service';
import { SuggestionsService } from './shared/services/suggestions.service';
import { DataBarchartComponent } from './pages/result/data-barchart/data-barchart.component';
import { DataStockchartComponent } from './pages/result/data-stockchart/data-stockchart.component';
import { DataLinechartComponent } from './pages/result/data-linechart/data-linechart.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ResultComponent,
    DataTableComponent,
    DataMapComponent,
    DataGraphComponent,
    GraphComponent,
    ErrorComponent,
    ...SHARED_VISUALS,
    ...D3_DIRECTIVES,
    DataCardComponent,
    DataGeneratorComponent,
    SuggestionsComponent,
    DataBarchartComponent,
    DataStockchartComponent,
    DataLinechartComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FlexLayoutModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatSidenavModule,
    MatListModule,
    MatButtonModule,
    MatDialogModule,
    MatIconModule,
    MatInputModule,
    MatFormFieldModule,
    MatPaginatorModule,
    MatTableModule,
    MatSelectModule,
    CdkTableModule,
    HttpClientModule,
    MatAutocompleteModule,
    FormsModule,
    ReactiveFormsModule,
    MatExpansionModule,
    MatBadgeModule,
    MatTabsModule,
    MatSliderModule,
    MatButtonToggleModule,
    MatSnackBarModule,
    MatChipsModule,
    MatSlideToggleModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyCGPvtJZ6awCs3FXvm1FJban8fjTmC_zEY'
    }),
    ChartModule
  ],
  exports: [
    MatPaginatorModule,
  ],
  providers: [
    D3Service,
    ConfigService,
    SuggestionsService,
    ConfigModule.init(),
    { provide: HIGHCHARTS_MODULES, useFactory: () => [more, exporting] }
],
  bootstrap: [AppComponent]
})

export class AppModule { }
