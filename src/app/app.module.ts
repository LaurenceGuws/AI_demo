import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';  
import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';  // Import BrowserAnimationsModule

import { AppComponent } from './app.component';
import { ChatComponent } from './chat/chat.component';
import { MessageInputComponent } from './message-input/message-input.component';
import { OptionsComponent } from './options/options.component';
import { PastConversationsComponent } from './past-conversations/past-conversations.component';
import { ContainerComponent } from './container/container.component';

@NgModule({
  declarations: [
    AppComponent,
    ChatComponent,
    MessageInputComponent,
    OptionsComponent,
    PastConversationsComponent,
    ContainerComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    BrowserAnimationsModule  // Include BrowserAnimationsModule in the imports array
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
