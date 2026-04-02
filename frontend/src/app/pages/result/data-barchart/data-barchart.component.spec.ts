import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DataBarchartComponent } from './data-barchart.component';

describe('DataBarchartComponent', () => {
  let component: DataBarchartComponent;
  let fixture: ComponentFixture<DataBarchartComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DataBarchartComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DataBarchartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
