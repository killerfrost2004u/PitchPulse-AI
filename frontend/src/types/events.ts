export interface TacticalEvent {
    event_id: string;
    timestamp: number;
    event_type: string;
    description: string;
    involved_entity_ids: number[];
}
