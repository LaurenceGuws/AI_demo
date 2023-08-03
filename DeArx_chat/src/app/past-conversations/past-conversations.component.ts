import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-past-conversations',
  templateUrl: './past-conversations.component.html',
  styleUrls: ['./past-conversations.component.css']
})
export class PastConversationsComponent implements OnInit {
  conversations = ['Conversation 1', 'Conversation 2', 'Conversation 3'];

  constructor() { }

  ngOnInit(): void {
  }
}
