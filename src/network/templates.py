"""
ClickSUMO - Network Templates
==============================

Pre-built network templates for common scenarios.
Users can generate complete networks with one click.

Author: Mahbub Hassan
Graduate Student & Non Asean Scholar
Department of Civil Engineering
Chulalongkorn University, Bangkok, Thailand

Copyright © 2026 Mahbub Hassan
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import math

from src.core.xml_generators import (
    Node, Edge, Phase, TrafficLight, 
    NetworkGenerator, kmh_to_ms
)


@dataclass
class NetworkTemplate:
    """Base class for network templates."""
    name: str
    description: str
    
    def generate(self) -> NetworkGenerator:
        """Generate the network. Override in subclasses."""
        raise NotImplementedError


class FourWayIntersection(NetworkTemplate):
    """
    Standard 4-way signalized intersection.
    
         N
         |
    W ---+--- E
         |
         S
    """
    
    def __init__(self,
                 arm_length: float = 200.0,
                 lanes_per_arm: int = 2,
                 speed_limit: float = 50.0,  # km/h
                 signal_type: str = "static",
                 green_time_ns: int = 30,
                 green_time_ew: int = 30,
                 yellow_time: int = 3):
        """
        Initialize 4-way intersection template.
        
        Args:
            arm_length: Length of each approach arm in meters
            lanes_per_arm: Number of lanes in each direction
            speed_limit: Speed limit in km/h
            signal_type: Traffic light type (static, actuated, delay_based)
            green_time_ns: Green time for North-South in seconds
            green_time_ew: Green time for East-West in seconds
            yellow_time: Yellow time in seconds
        """
        super().__init__(
            name="4-Way Intersection",
            description="Standard signalized 4-way intersection"
        )
        self.arm_length = arm_length
        self.lanes_per_arm = lanes_per_arm
        self.speed_limit = speed_limit
        self.signal_type = signal_type
        self.green_time_ns = green_time_ns
        self.green_time_ew = green_time_ew
        self.yellow_time = yellow_time
    
    def generate(self) -> NetworkGenerator:
        """Generate the 4-way intersection network."""
        network = NetworkGenerator()
        speed = kmh_to_ms(self.speed_limit)
        
        # Add center node (traffic light)
        network.add_node(Node(
            id="C",
            x=0,
            y=0,
            node_type="traffic_light",
            tl_type=self.signal_type
        ))
        
        # Add approach nodes
        network.add_node(Node("N", 0, self.arm_length, "priority"))
        network.add_node(Node("S", 0, -self.arm_length, "priority"))
        network.add_node(Node("E", self.arm_length, 0, "priority"))
        network.add_node(Node("W", -self.arm_length, 0, "priority"))
        
        # Add edges (bidirectional roads)
        edges = [
            ("N2C", "N", "C"),
            ("C2N", "C", "N"),
            ("S2C", "S", "C"),
            ("C2S", "C", "S"),
            ("E2C", "E", "C"),
            ("C2E", "C", "E"),
            ("W2C", "W", "C"),
            ("C2W", "C", "W"),
        ]
        
        for edge_id, from_node, to_node in edges:
            network.add_edge(Edge(
                id=edge_id,
                from_node=from_node,
                to_node=to_node,
                num_lanes=self.lanes_per_arm,
                speed=speed,
                priority=1
            ))
        
        # Generate traffic light state strings
        # Each lane needs a character: G=green, r=red, y=yellow
        # Order: N2C lanes, S2C lanes, E2C lanes, W2C lanes (for each direction)
        n = self.lanes_per_arm
        
        # NS green, EW red
        ns_green = "G" * (n * 2) + "r" * (n * 2) + "G" * (n * 2) + "r" * (n * 2)
        ns_yellow = "y" * (n * 2) + "r" * (n * 2) + "y" * (n * 2) + "r" * (n * 2)
        
        # EW green, NS red
        ew_green = "r" * (n * 2) + "G" * (n * 2) + "r" * (n * 2) + "G" * (n * 2)
        ew_yellow = "r" * (n * 2) + "y" * (n * 2) + "r" * (n * 2) + "y" * (n * 2)
        
        # Create traffic light program
        tl = TrafficLight(
            id="C",
            tl_type=self.signal_type,
            phases=[
                Phase(self.green_time_ns, ns_green, name="NS_Green"),
                Phase(self.yellow_time, ns_yellow, name="NS_Yellow"),
                Phase(self.green_time_ew, ew_green, name="EW_Green"),
                Phase(self.yellow_time, ew_yellow, name="EW_Yellow"),
            ]
        )
        network.add_traffic_light(tl)
        
        return network


class ThreeWayIntersection(NetworkTemplate):
    """
    T-intersection (3-way).
    
         N
         |
    W ---+--- E
    """
    
    def __init__(self,
                 arm_length: float = 200.0,
                 lanes_per_arm: int = 2,
                 speed_limit: float = 50.0,
                 has_signal: bool = True):
        super().__init__(
            name="3-Way T-Intersection",
            description="T-intersection (3-way)"
        )
        self.arm_length = arm_length
        self.lanes_per_arm = lanes_per_arm
        self.speed_limit = speed_limit
        self.has_signal = has_signal
    
    def generate(self) -> NetworkGenerator:
        network = NetworkGenerator()
        speed = kmh_to_ms(self.speed_limit)
        
        node_type = "traffic_light" if self.has_signal else "priority"
        
        # Add nodes
        network.add_node(Node("C", 0, 0, node_type))
        network.add_node(Node("N", 0, self.arm_length, "priority"))
        network.add_node(Node("E", self.arm_length, 0, "priority"))
        network.add_node(Node("W", -self.arm_length, 0, "priority"))
        
        # Add edges
        edges = [
            ("N2C", "N", "C"),
            ("C2N", "C", "N"),
            ("E2C", "E", "C"),
            ("C2E", "C", "E"),
            ("W2C", "W", "C"),
            ("C2W", "C", "W"),
        ]
        
        for edge_id, from_node, to_node in edges:
            network.add_edge(Edge(
                id=edge_id,
                from_node=from_node,
                to_node=to_node,
                num_lanes=self.lanes_per_arm,
                speed=speed
            ))
        
        if self.has_signal:
            n = self.lanes_per_arm
            tl = TrafficLight("C", phases=[
                Phase(30, "G" * (n*2) + "r" * (n*2) + "r" * (n*2)),
                Phase(3, "y" * (n*2) + "r" * (n*2) + "r" * (n*2)),
                Phase(30, "r" * (n*2) + "G" * (n*2) + "G" * (n*2)),
                Phase(3, "r" * (n*2) + "y" * (n*2) + "y" * (n*2)),
            ])
            network.add_traffic_light(tl)
        
        return network


class Roundabout(NetworkTemplate):
    """
    Roundabout with configurable number of arms.
    
          N
          |
     NW --+-- NE
          O
     SW --+-- SE
          |
          S
    """
    
    def __init__(self,
                 num_arms: int = 4,
                 radius: float = 30.0,
                 arm_length: float = 200.0,
                 lanes_per_arm: int = 1,
                 roundabout_lanes: int = 2,
                 speed_limit: float = 30.0):
        super().__init__(
            name=f"{num_arms}-Arm Roundabout",
            description=f"Roundabout with {num_arms} entry/exit arms"
        )
        self.num_arms = num_arms
        self.radius = radius
        self.arm_length = arm_length
        self.lanes_per_arm = lanes_per_arm
        self.roundabout_lanes = roundabout_lanes
        self.speed_limit = speed_limit
    
    def generate(self) -> NetworkGenerator:
        network = NetworkGenerator()
        speed = kmh_to_ms(self.speed_limit)
        
        # Calculate positions for roundabout nodes
        angles = [i * (360 / self.num_arms) for i in range(self.num_arms)]
        
        # Add roundabout internal nodes
        for i, angle in enumerate(angles):
            rad = math.radians(angle - 90)  # Start from North
            x = self.radius * math.cos(rad)
            y = self.radius * math.sin(rad)
            network.add_node(Node(f"R{i}", x, y, "priority"))
        
        # Add approach nodes
        for i, angle in enumerate(angles):
            rad = math.radians(angle - 90)
            x = (self.radius + self.arm_length) * math.cos(rad)
            y = (self.radius + self.arm_length) * math.sin(rad)
            network.add_node(Node(f"A{i}", x, y, "priority"))
        
        # Add roundabout edges (circular)
        for i in range(self.num_arms):
            next_i = (i + 1) % self.num_arms
            network.add_edge(Edge(
                f"R{i}2R{next_i}",
                f"R{i}",
                f"R{next_i}",
                num_lanes=self.roundabout_lanes,
                speed=speed
            ))
        
        # Add approach/exit edges
        for i in range(self.num_arms):
            # Entry
            network.add_edge(Edge(
                f"A{i}2R{i}",
                f"A{i}",
                f"R{i}",
                num_lanes=self.lanes_per_arm,
                speed=speed
            ))
            # Exit
            network.add_edge(Edge(
                f"R{i}2A{i}",
                f"R{i}",
                f"A{i}",
                num_lanes=self.lanes_per_arm,
                speed=speed
            ))
        
        return network


class GridNetwork(NetworkTemplate):
    """
    Grid network with specified dimensions.
    
    +---+---+---+
    |   |   |   |
    +---+---+---+
    |   |   |   |
    +---+---+---+
    """
    
    def __init__(self,
                 rows: int = 3,
                 cols: int = 3,
                 block_length: float = 200.0,
                 lanes: int = 2,
                 speed_limit: float = 50.0,
                 signalized: bool = True):
        super().__init__(
            name=f"{rows}x{cols} Grid Network",
            description=f"Grid network with {rows} rows and {cols} columns"
        )
        self.rows = rows
        self.cols = cols
        self.block_length = block_length
        self.lanes = lanes
        self.speed_limit = speed_limit
        self.signalized = signalized
    
    def generate(self) -> NetworkGenerator:
        network = NetworkGenerator()
        speed = kmh_to_ms(self.speed_limit)
        
        # Add nodes
        for row in range(self.rows):
            for col in range(self.cols):
                node_id = f"n{row}_{col}"
                x = col * self.block_length
                y = row * self.block_length
                
                # Determine if it's an intersection (not on edge)
                is_edge = (row == 0 or row == self.rows - 1 or 
                          col == 0 or col == self.cols - 1)
                
                if is_edge or not self.signalized:
                    node_type = "priority"
                else:
                    node_type = "traffic_light"
                
                network.add_node(Node(node_id, x, y, node_type))
        
        # Add horizontal edges
        for row in range(self.rows):
            for col in range(self.cols - 1):
                from_id = f"n{row}_{col}"
                to_id = f"n{row}_{col + 1}"
                
                # Eastbound
                network.add_edge(Edge(
                    f"e{row}_{col}_EB",
                    from_id,
                    to_id,
                    num_lanes=self.lanes,
                    speed=speed
                ))
                
                # Westbound
                network.add_edge(Edge(
                    f"e{row}_{col}_WB",
                    to_id,
                    from_id,
                    num_lanes=self.lanes,
                    speed=speed
                ))
        
        # Add vertical edges
        for row in range(self.rows - 1):
            for col in range(self.cols):
                from_id = f"n{row}_{col}"
                to_id = f"n{row + 1}_{col}"
                
                # Northbound
                network.add_edge(Edge(
                    f"e{row}_{col}_NB",
                    from_id,
                    to_id,
                    num_lanes=self.lanes,
                    speed=speed
                ))
                
                # Southbound
                network.add_edge(Edge(
                    f"e{row}_{col}_SB",
                    to_id,
                    from_id,
                    num_lanes=self.lanes,
                    speed=speed
                ))
        
        # Add traffic lights to internal intersections
        if self.signalized:
            for row in range(1, self.rows - 1):
                for col in range(1, self.cols - 1):
                    tl_id = f"n{row}_{col}"
                    n = self.lanes
                    
                    # Simple 2-phase signal
                    tl = TrafficLight(
                        id=tl_id,
                        phases=[
                            Phase(30, "G" * (n*4) + "r" * (n*4)),  # NS
                            Phase(3, "y" * (n*4) + "r" * (n*4)),
                            Phase(30, "r" * (n*4) + "G" * (n*4)),  # EW
                            Phase(3, "r" * (n*4) + "y" * (n*4)),
                        ]
                    )
                    network.add_traffic_light(tl)
        
        return network


class Corridor(NetworkTemplate):
    """
    Arterial corridor with multiple intersections.
    
    o---+---+---+---+---o
        ^   ^   ^   ^
       cross streets
    """
    
    def __init__(self,
                 num_intersections: int = 5,
                 spacing: float = 300.0,
                 main_lanes: int = 3,
                 cross_lanes: int = 2,
                 main_speed: float = 60.0,
                 cross_speed: float = 40.0,
                 signalized: bool = True):
        super().__init__(
            name=f"Arterial Corridor ({num_intersections} intersections)",
            description="Linear corridor with signalized intersections"
        )
        self.num_intersections = num_intersections
        self.spacing = spacing
        self.main_lanes = main_lanes
        self.cross_lanes = cross_lanes
        self.main_speed = main_speed
        self.cross_speed = cross_speed
        self.signalized = signalized
    
    def generate(self) -> NetworkGenerator:
        network = NetworkGenerator()
        main_speed = kmh_to_ms(self.main_speed)
        cross_speed = kmh_to_ms(self.cross_speed)
        
        cross_arm_length = 150.0
        
        # Add main corridor nodes
        for i in range(self.num_intersections + 2):
            x = i * self.spacing
            
            if i == 0 or i == self.num_intersections + 1:
                # End nodes
                network.add_node(Node(f"M{i}", x, 0, "priority"))
            else:
                # Intersection nodes
                node_type = "traffic_light" if self.signalized else "priority"
                network.add_node(Node(f"M{i}", x, 0, node_type))
                
                # Cross street nodes
                network.add_node(Node(f"N{i}", x, cross_arm_length, "priority"))
                network.add_node(Node(f"S{i}", x, -cross_arm_length, "priority"))
        
        # Add main corridor edges
        for i in range(self.num_intersections + 1):
            from_id = f"M{i}"
            to_id = f"M{i + 1}"
            
            # Eastbound
            network.add_edge(Edge(
                f"main_{i}_EB",
                from_id,
                to_id,
                num_lanes=self.main_lanes,
                speed=main_speed
            ))
            
            # Westbound
            network.add_edge(Edge(
                f"main_{i}_WB",
                to_id,
                from_id,
                num_lanes=self.main_lanes,
                speed=main_speed
            ))
        
        # Add cross streets
        for i in range(1, self.num_intersections + 1):
            main_id = f"M{i}"
            north_id = f"N{i}"
            south_id = f"S{i}"
            
            # Northbound
            network.add_edge(Edge(
                f"cross_{i}_NB",
                south_id,
                main_id,
                num_lanes=self.cross_lanes,
                speed=cross_speed
            ))
            network.add_edge(Edge(
                f"cross_{i}_NB2",
                main_id,
                north_id,
                num_lanes=self.cross_lanes,
                speed=cross_speed
            ))
            
            # Southbound
            network.add_edge(Edge(
                f"cross_{i}_SB",
                north_id,
                main_id,
                num_lanes=self.cross_lanes,
                speed=cross_speed
            ))
            network.add_edge(Edge(
                f"cross_{i}_SB2",
                main_id,
                south_id,
                num_lanes=self.cross_lanes,
                speed=cross_speed
            ))
            
            # Add traffic light
            if self.signalized:
                n_main = self.main_lanes
                n_cross = self.cross_lanes
                
                tl = TrafficLight(
                    id=main_id,
                    phases=[
                        Phase(40, "G" * (n_main*4) + "r" * (n_cross*4)),  # Main
                        Phase(3, "y" * (n_main*4) + "r" * (n_cross*4)),
                        Phase(25, "r" * (n_main*4) + "G" * (n_cross*4)),  # Cross
                        Phase(3, "r" * (n_main*4) + "y" * (n_cross*4)),
                    ]
                )
                network.add_traffic_light(tl)
        
        return network


class Highway(NetworkTemplate):
    """
    Highway/freeway segment with optional on/off ramps.
    
    Entry ----====----====---- Exit
              ramp    ramp
    """
    
    def __init__(self,
                 length: float = 2000.0,
                 lanes: int = 3,
                 speed_limit: float = 100.0,
                 num_ramps: int = 2,
                 ramp_lanes: int = 1):
        super().__init__(
            name="Highway Segment",
            description=f"Highway with {lanes} lanes and {num_ramps} ramp pairs"
        )
        self.length = length
        self.lanes = lanes
        self.speed_limit = speed_limit
        self.num_ramps = num_ramps
        self.ramp_lanes = ramp_lanes
    
    def generate(self) -> NetworkGenerator:
        network = NetworkGenerator()
        speed = kmh_to_ms(self.speed_limit)
        ramp_speed = kmh_to_ms(60)
        
        # Calculate ramp positions
        ramp_spacing = self.length / (self.num_ramps + 1)
        
        # Add main highway nodes
        network.add_node(Node("start", 0, 0, "priority"))
        network.add_node(Node("end", self.length, 0, "priority"))
        
        # Add ramp junction nodes
        for i in range(1, self.num_ramps + 1):
            x = i * ramp_spacing
            network.add_node(Node(f"junc_{i}", x, 0, "priority"))
            network.add_node(Node(f"on_ramp_{i}", x - 100, -100, "priority"))
            network.add_node(Node(f"off_ramp_{i}", x + 100, -100, "priority"))
        
        # Add main highway edges
        prev_node = "start"
        for i in range(1, self.num_ramps + 1):
            junc = f"junc_{i}"
            network.add_edge(Edge(
                f"hw_{prev_node}_{junc}",
                prev_node,
                junc,
                num_lanes=self.lanes,
                speed=speed,
                priority=3
            ))
            prev_node = junc
        
        network.add_edge(Edge(
            f"hw_{prev_node}_end",
            prev_node,
            "end",
            num_lanes=self.lanes,
            speed=speed,
            priority=3
        ))
        
        # Add ramps
        for i in range(1, self.num_ramps + 1):
            junc = f"junc_{i}"
            
            # On-ramp
            network.add_edge(Edge(
                f"on_ramp_{i}",
                f"on_ramp_{i}",
                junc,
                num_lanes=self.ramp_lanes,
                speed=ramp_speed
            ))
            
            # Off-ramp
            network.add_edge(Edge(
                f"off_ramp_{i}",
                junc,
                f"off_ramp_{i}",
                num_lanes=self.ramp_lanes,
                speed=ramp_speed
            ))
        
        return network


# =============================================================================
# TEMPLATE REGISTRY
# =============================================================================

TEMPLATES = {
    "4way": FourWayIntersection,
    "3way": ThreeWayIntersection,
    "roundabout": Roundabout,
    "grid": GridNetwork,
    "corridor": Corridor,
    "highway": Highway,
}


def list_templates() -> List[Dict]:
    """List all available templates."""
    result = []
    for key, template_class in TEMPLATES.items():
        # Create instance with defaults to get name/description
        instance = template_class()
        result.append({
            "key": key,
            "name": instance.name,
            "description": instance.description,
        })
    return result


def create_network(template_key: str, **kwargs) -> NetworkGenerator:
    """
    Create a network from a template.
    
    Args:
        template_key: Template identifier (e.g., "4way", "grid")
        **kwargs: Template-specific parameters
    
    Returns:
        NetworkGenerator with the network ready to save
    """
    if template_key not in TEMPLATES:
        raise ValueError(f"Unknown template: {template_key}. "
                        f"Available: {list(TEMPLATES.keys())}")
    
    template = TEMPLATES[template_key](**kwargs)
    return template.generate()


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("Available templates:")
    for t in list_templates():
        print(f"  - {t['key']}: {t['name']} - {t['description']}")
    
    print("\n" + "="*50)
    print("Creating 4-way intersection...")
    
    network = create_network(
        "4way",
        arm_length=200,
        lanes_per_arm=2,
        speed_limit=50,
        green_time_ns=35,
        green_time_ew=25
    )
    
    network.save_all("./outputs", "4way_intersection")
    print("✅ Saved to ./outputs/4way_intersection.*")
    
    print("\n" + "="*50)
    print("Creating 3x3 grid network...")
    
    network = create_network(
        "grid",
        rows=3,
        cols=3,
        block_length=200,
        lanes=2,
        signalized=True
    )
    
    network.save_all("./outputs", "grid_3x3")
    print("✅ Saved to ./outputs/grid_3x3.*")
