import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PastConversationsComponent } from './past-conversations.component';

describe('PastConversationsComponent', () => {
  let component: PastConversationsComponent;
  let fixture: ComponentFixture<PastConversationsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PastConversationsComponent]
    });
    fixture = TestBed.createComponent(PastConversationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
