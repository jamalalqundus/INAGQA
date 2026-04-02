/**
 * Name:     app-routing.module.ts
 * Author:   ssa
 * 
 * Description: The routing module assigns the corresponding component 
 *  to be rendered to the browser url.
 * 
 * 
*/

import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { ResultComponent } from './pages/result/result.component';


const routes: Routes = [

  {path: '' , component: HomeComponent},
  {path: 'home' , component: HomeComponent},
  {path: 'result/:tab/:query' , component: ResultComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
