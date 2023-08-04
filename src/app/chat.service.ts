import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { HttpClient } from '@angular/common/http';

interface Message {
  role: string;
  content: string;
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private messagesSource = new BehaviorSubject<Message[]>([]);
  currentMessages = this.messagesSource.asObservable();

  constructor(private http: HttpClient) { }

  addMessage(message: Message) {
    this.messagesSource.next([...this.messagesSource.value, message]);
    this.getMessages(message);
  }

  setMessages(messages: Message[]) {
    console.log('Setting messages in service:', messages);
    this.messagesSource.next(messages);
  }

  clearMessages() {
    this.messagesSource.next([]);
  }

  getMessages(message: Message) {
    this.http.post('http://localhost:30000/message', {message: message}).subscribe(
      (data: any) => {
        console.log("Data received from server: ", data);
        if (data && data.messages && Array.isArray(data.messages)) {
          console.log('Updating messages in service with server response:', data.messages);
          this.setMessages(data.messages);
        } else {
          console.error("Unexpected server response. 'messages' is undefined or not an array.");
        }
      },
      error => {
        console.error('Error:', error);
      }
    );
  }
}
