export interface Entity {
    id: number;
    label: "player" | "referee" | "ball";
    team?: "team_a" | "team_b" | null;
    position: [number, number]; // [x, y] coordinates
    speed?: number;
}

export interface FrameData {
    frame_id: number;
    timestamp: number;
    entities: Entity[];
}
