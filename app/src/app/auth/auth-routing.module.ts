import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'sign_in',
    loadChildren: ()=> import('./sign-in/sign-in.module').then(m => m.SignInPageModule)
  },
  {
    path: 'sign_up',
    loadChildren: ()=> import('./sign-up/sign-up.module').then(m => m.SignUpPageModule) 
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AuthRoutingModule { }
