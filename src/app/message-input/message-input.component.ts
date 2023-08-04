import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ChatService } from '../chat.service';

@Component({
  selector: 'app-message-input',
  templateUrl: './message-input.component.html',
  styleUrls: ['./message-input.component.css']
})
export class MessageInputComponent implements OnInit {
  message = '';

  constructor(private http: HttpClient, private chatService: ChatService) {}

  ngOnInit(): void {}

  sendMessage(): void {
    if (!this.message) {
      return;
    }

    this.chatService.addMessage({ role: 'user', content: this.message });
    this.message = '';
  }
}
