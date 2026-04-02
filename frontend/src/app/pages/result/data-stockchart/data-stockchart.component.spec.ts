import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DataStockchartComponent } from './data-stockchart.component';

describe('DataStockchartComponent', () => {
  let component: DataStockchartComponent;
  let fixture: ComponentFixture<DataStockchartComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DataStockchartComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DataStockchartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
