import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

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

  constructor() { }

  changeMessages(messages: Message[]) {
    this.messagesSource.next(messages);
  }

  setMessages(messages: Message[]) {
    this.messagesSource.next(messages);
  }

  clearMessages() {
    this.messagesSource.next([]);
  }
}
