
import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface Message {
  role: string;
  content: string;
  // Include any other properties you expect a message to have.
}

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  messages: Message[] = [];

  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.getMessages();
  }

  getMessages() {
    this.http.get('http://localhost:30000/conversations').subscribe(
      (data: any) => {
        this.messages = data.conversations;
      },
      error => {
        console.error('Error:', error);
      }
    );
  }
}
