import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ChatService } from '../chat.service';  // Import the ChatService

@Component({
  selector: 'app-past-conversations',
  templateUrl: './past-conversations.component.html',
  styleUrls: ['./past-conversations.component.css']
})
export class PastConversationsComponent implements OnInit {
  conversations = [];

  constructor(private http: HttpClient, private chatService: ChatService) { }  // Inject the ChatService

  ngOnInit(): void {
    this.getConversations();
  }

  getConversations(): void {
    this.http.get('http://localhost:30000/conversations').subscribe(
      (data: any) => {
        this.conversations = data.conversations;
      },
      error => {
        console.error('Error:', error);
      }
    );
  }

  getConversation(name: string): void {  // Add this method
    this.http.get(`http://localhost:30000/conversations/${name}`).subscribe(
      (data: any) => {
        this.chatService.setMessages(data.messages);
      },
      error => {
        console.error('Error:', error);
      }
    );
  }
}
