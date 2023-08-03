import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { ChatComponent } from './chat/chat.component';
import { MessageInputComponent } from './message-input/message-input.component';
import { OptionsComponent } from './options/options.component';
import { HttpClientModule } from '@angular/common/http';  
import { FormsModule } from '@angular/forms';
import { PastConversationsComponent } from './past-conversations/past-conversations.component';  // <-- import FormsModule here

@NgModule({
  declarations: [
    AppComponent,
    ChatComponent,
    MessageInputComponent,
    OptionsComponent,
    PastConversationsComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule  // <-- and include it in the imports array
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
