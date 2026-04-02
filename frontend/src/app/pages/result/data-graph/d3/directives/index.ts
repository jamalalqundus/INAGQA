import { ZoomableDirective } from './zoomable.directive';
import { DraggableDirective } from './draggable.directive';
import { ClickableDirective } from './clickable.directive';

export * from './zoomable.directive';
export * from './draggable.directive';
export * from './clickable.directive';

export const D3_DIRECTIVES = [
    ZoomableDirective,
    DraggableDirective,
    ClickableDirective
];