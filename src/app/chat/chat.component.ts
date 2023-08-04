import { Component, OnInit } from '@angular/core';
import { filter } from 'rxjs/operators';
import { ChatService } from '../chat.service';

interface Message {
  role: string;
  content: string;
}

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  messages: Message[] = [];

  constructor(private chatService: ChatService) {
    this.chatService.currentMessages
      .pipe(filter(messages => !!messages && messages.length > 0))
      .subscribe(messages => {
        console.log('Received messages from service:', messages);
        this.messages = messages;
      });
  }

  ngOnInit() {}
}
