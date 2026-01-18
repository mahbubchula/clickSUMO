"""
ClickSUMO - SUMO XML Generators
================================

Core classes for generating all SUMO XML files.
This is the heart of ClickSUMO - users work with simple Python objects,
and these generators create the complex XML that SUMO needs.

Author: Mahbub Hassan
Graduate Student & Non Asean Scholar
Department of Civil Engineering
Chulalongkorn University, Bangkok, Thailand

Copyright © 2026 Mahbub Hassan
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
import math


# =============================================================================
# DATA CLASSES - Simple Python objects that represent SUMO elements
# =============================================================================

@dataclass
class Node:
    """Represents a junction/node in the network."""
    id: str
    x: float
    y: float
    node_type: str = "priority"  # priority, traffic_light, right_before_left, unregulated
    tl_type: str = ""  # static, actuated, delay_based, NEMA

    def __post_init__(self):
        """Validate node data."""
        if not self.id or not isinstance(self.id, str):
            raise ValueError("Node ID must be a non-empty string")
        if not isinstance(self.x, (int, float)) or not isinstance(self.y, (int, float)):
            raise ValueError("Node coordinates must be numeric")
        valid_types = ["priority", "traffic_light", "right_before_left", "unregulated", "dead_end"]
        if self.node_type not in valid_types:
            raise ValueError(f"Invalid node_type. Must be one of: {valid_types}")

    def to_xml_attrib(self) -> Dict:
        """Convert to XML attributes."""
        attrib = {
            "id": self.id,
            "x": str(self.x),
            "y": str(self.y),
            "type": self.node_type,
        }
        if self.node_type == "traffic_light" and self.tl_type:
            attrib["tlType"] = self.tl_type
        return attrib


@dataclass
class Edge:
    """Represents a road/edge in the network."""
    id: str
    from_node: str
    to_node: str
    num_lanes: int = 1
    speed: float = 13.89  # m/s (50 km/h)
    priority: int = 1
    edge_type: str = ""
    allow: str = ""  # Vehicle classes allowed
    disallow: str = ""  # Vehicle classes disallowed

    def __post_init__(self):
        """Validate edge data."""
        if not self.id or not isinstance(self.id, str):
            raise ValueError("Edge ID must be a non-empty string")
        if not self.from_node or not isinstance(self.from_node, str):
            raise ValueError("from_node must be a non-empty string")
        if not self.to_node or not isinstance(self.to_node, str):
            raise ValueError("to_node must be a non-empty string")
        if self.from_node == self.to_node:
            raise ValueError(f"Edge cannot connect node to itself: {self.from_node}")
        if not isinstance(self.num_lanes, int) or self.num_lanes < 1:
            raise ValueError("num_lanes must be a positive integer")
        if not isinstance(self.speed, (int, float)) or self.speed <= 0:
            raise ValueError("speed must be a positive number")
        if not isinstance(self.priority, int):
            raise ValueError("priority must be an integer")

    def to_xml_attrib(self) -> Dict:
        """Convert to XML attributes."""
        attrib = {
            "id": self.id,
            "from": self.from_node,
            "to": self.to_node,
            "numLanes": str(self.num_lanes),
            "speed": str(self.speed),
            "priority": str(self.priority),
        }
        if self.edge_type:
            attrib["type"] = self.edge_type
        if self.allow:
            attrib["allow"] = self.allow
        if self.disallow:
            attrib["disallow"] = self.disallow
        return attrib


@dataclass
class Connection:
    """Represents a connection between lanes at junctions."""
    from_edge: str
    to_edge: str
    from_lane: int
    to_lane: int
    
    def to_xml_attrib(self) -> Dict:
        return {
            "from": self.from_edge,
            "to": self.to_edge,
            "fromLane": str(self.from_lane),
            "toLane": str(self.to_lane),
        }


@dataclass
class Phase:
    """Represents a traffic light phase."""
    duration: int
    state: str  # e.g., "GGGrrrGGGrrr"
    min_dur: int = 0
    max_dur: int = 0
    name: str = ""

    def __post_init__(self):
        """Validate phase data."""
        if not isinstance(self.duration, int) or self.duration <= 0:
            raise ValueError("Phase duration must be a positive integer")
        if not self.state or not isinstance(self.state, str):
            raise ValueError("Phase state must be a non-empty string")
        if self.min_dur < 0:
            raise ValueError("min_dur cannot be negative")
        if self.max_dur < 0:
            raise ValueError("max_dur cannot be negative")
        if self.max_dur > 0 and self.min_dur > 0 and self.min_dur > self.max_dur:
            raise ValueError("min_dur cannot be greater than max_dur")

    def to_xml_attrib(self) -> Dict:
        attrib = {
            "duration": str(self.duration),
            "state": self.state,
        }
        if self.min_dur > 0:
            attrib["minDur"] = str(self.min_dur)
        if self.max_dur > 0:
            attrib["maxDur"] = str(self.max_dur)
        if self.name:
            attrib["name"] = self.name
        return attrib


@dataclass
class TrafficLight:
    """Represents a complete traffic light program."""
    id: str
    phases: List[Phase]
    tl_type: str = "static"  # static, actuated, delay_based, NEMA
    program_id: str = "0"
    offset: int = 0
    
    def to_xml_element(self) -> ET.Element:
        """Convert to XML element."""
        tl = ET.Element("tlLogic")
        tl.set("id", self.id)
        tl.set("type", self.tl_type)
        tl.set("programID", self.program_id)
        tl.set("offset", str(self.offset))
        
        for phase in self.phases:
            phase_elem = ET.SubElement(tl, "phase")
            for key, value in phase.to_xml_attrib().items():
                phase_elem.set(key, value)
        
        return tl


@dataclass
class VehicleType:
    """Represents a vehicle type definition."""
    id: str
    length: float = 5.0
    min_gap: float = 2.5
    max_speed: float = 55.56  # m/s (200 km/h)
    accel: float = 2.6
    decel: float = 4.5
    sigma: float = 0.5  # Driver imperfection
    tau: float = 1.0  # Reaction time
    vclass: str = "passenger"
    color: str = ""
    emission_class: str = "HBEFA3/PC_G_EU4"
    car_follow_model: str = ""  # Krauss, IDM, EIDM, etc.
    
    def to_xml_element(self) -> ET.Element:
        """Convert to XML element."""
        vtype = ET.Element("vType")
        vtype.set("id", self.id)
        vtype.set("length", str(self.length))
        vtype.set("minGap", str(self.min_gap))
        vtype.set("maxSpeed", str(self.max_speed))
        vtype.set("accel", str(self.accel))
        vtype.set("decel", str(self.decel))
        vtype.set("sigma", str(self.sigma))
        vtype.set("tau", str(self.tau))
        vtype.set("vClass", self.vclass)
        vtype.set("emissionClass", self.emission_class)
        
        if self.color:
            vtype.set("color", self.color)
        if self.car_follow_model:
            vtype.set("carFollowModel", self.car_follow_model)
        
        return vtype


@dataclass
class Route:
    """Represents a route (sequence of edges)."""
    id: str
    edges: List[str]
    
    def to_xml_element(self) -> ET.Element:
        route = ET.Element("route")
        route.set("id", self.id)
        route.set("edges", " ".join(self.edges))
        return route


@dataclass
class Vehicle:
    """Represents a single vehicle."""
    id: str
    route_id: str = ""
    route_edges: List[str] = field(default_factory=list)
    vtype: str = "DEFAULT_VEHTYPE"
    depart: str = "0"
    depart_lane: str = "best"
    depart_speed: str = "max"
    
    def to_xml_element(self) -> ET.Element:
        veh = ET.Element("vehicle")
        veh.set("id", self.id)
        veh.set("type", self.vtype)
        veh.set("depart", self.depart)
        veh.set("departLane", self.depart_lane)
        veh.set("departSpeed", self.depart_speed)
        
        if self.route_id:
            veh.set("route", self.route_id)
        elif self.route_edges:
            route = ET.SubElement(veh, "route")
            route.set("edges", " ".join(self.route_edges))
        
        return veh


@dataclass
class Flow:
    """Represents a traffic flow (repeated vehicles)."""
    id: str
    from_edge: str = ""
    to_edge: str = ""
    route_id: str = ""
    vtype: str = "DEFAULT_VEHTYPE"
    begin: float = 0
    end: float = 3600
    vehs_per_hour: float = 0
    probability: float = 0
    period: float = 0
    number: int = 0
    
    def to_xml_element(self) -> ET.Element:
        flow = ET.Element("flow")
        flow.set("id", self.id)
        flow.set("type", self.vtype)
        flow.set("begin", str(self.begin))
        flow.set("end", str(self.end))
        
        if self.route_id:
            flow.set("route", self.route_id)
        else:
            if self.from_edge:
                flow.set("from", self.from_edge)
            if self.to_edge:
                flow.set("to", self.to_edge)
        
        # Only one of these should be set
        if self.vehs_per_hour > 0:
            flow.set("vehsPerHour", str(self.vehs_per_hour))
        elif self.probability > 0:
            flow.set("probability", str(self.probability))
        elif self.period > 0:
            flow.set("period", str(self.period))
        elif self.number > 0:
            flow.set("number", str(self.number))
        
        return flow


# =============================================================================
# XML GENERATORS - Convert Python objects to SUMO XML files
# =============================================================================

class XMLGenerator:
    """Base class for XML generation with pretty printing."""
    
    @staticmethod
    def prettify(elem: ET.Element) -> str:
        """Return a pretty-printed XML string."""
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="    ")
    
    @staticmethod
    def save(elem: ET.Element, filepath: str):
        """Save XML element to file with pretty formatting."""
        xml_string = XMLGenerator.prettify(elem)
        # Remove extra blank lines
        lines = [line for line in xml_string.split('\n') if line.strip()]
        with open(filepath, 'w') as f:
            f.write('\n'.join(lines))


class NetworkGenerator(XMLGenerator):
    """
    Generates SUMO network files (.nod.xml, .edg.xml, .con.xml, .tll.xml).
    
    These are "plain XML" files that netconvert uses to create the final .net.xml
    """
    
    def __init__(self):
        self.nodes: List[Node] = []
        self.edges: List[Edge] = []
        self.connections: List[Connection] = []
        self.traffic_lights: List[TrafficLight] = []
    
    def add_node(self, node: Node):
        """Add a node to the network."""
        self.nodes.append(node)
        return self
    
    def add_edge(self, edge: Edge):
        """Add an edge to the network."""
        self.edges.append(edge)
        return self
    
    def add_connection(self, connection: Connection):
        """Add a connection to the network."""
        self.connections.append(connection)
        return self
    
    def add_traffic_light(self, tl: TrafficLight):
        """Add a traffic light program."""
        self.traffic_lights.append(tl)
        return self
    
    def generate_nodes_xml(self) -> ET.Element:
        """Generate .nod.xml content."""
        root = ET.Element("nodes")
        for node in self.nodes:
            node_elem = ET.SubElement(root, "node")
            for key, value in node.to_xml_attrib().items():
                node_elem.set(key, value)
        return root
    
    def generate_edges_xml(self) -> ET.Element:
        """Generate .edg.xml content."""
        root = ET.Element("edges")
        for edge in self.edges:
            edge_elem = ET.SubElement(root, "edge")
            for key, value in edge.to_xml_attrib().items():
                edge_elem.set(key, value)
        return root
    
    def generate_connections_xml(self) -> ET.Element:
        """Generate .con.xml content."""
        root = ET.Element("connections")
        for conn in self.connections:
            conn_elem = ET.SubElement(root, "connection")
            for key, value in conn.to_xml_attrib().items():
                conn_elem.set(key, value)
        return root
    
    def generate_tll_xml(self) -> ET.Element:
        """Generate .tll.xml content (traffic light logic)."""
        root = ET.Element("tlLogics")
        for tl in self.traffic_lights:
            root.append(tl.to_xml_element())
        return root
    
    def save_all(self, base_path: str, name: str):
        """
        Save all network files.
        
        Args:
            base_path: Directory to save files
            name: Base name for files (e.g., "mynetwork" -> mynetwork.nod.xml, etc.)
        """
        import os
        os.makedirs(base_path, exist_ok=True)
        
        # Save nodes
        self.save(
            self.generate_nodes_xml(),
            os.path.join(base_path, f"{name}.nod.xml")
        )
        
        # Save edges
        self.save(
            self.generate_edges_xml(),
            os.path.join(base_path, f"{name}.edg.xml")
        )
        
        # Save connections (if any)
        if self.connections:
            self.save(
                self.generate_connections_xml(),
                os.path.join(base_path, f"{name}.con.xml")
            )
        
        # Save traffic lights (if any)
        if self.traffic_lights:
            self.save(
                self.generate_tll_xml(),
                os.path.join(base_path, f"{name}.tll.xml")
            )
        
        return self


class RouteGenerator(XMLGenerator):
    """
    Generates SUMO route files (.rou.xml).
    
    Contains vehicle types, routes, vehicles, and flows.
    """
    
    def __init__(self):
        self.vehicle_types: List[VehicleType] = []
        self.routes: List[Route] = []
        self.vehicles: List[Vehicle] = []
        self.flows: List[Flow] = []
    
    def add_vehicle_type(self, vtype: VehicleType):
        """Add a vehicle type."""
        self.vehicle_types.append(vtype)
        return self
    
    def add_route(self, route: Route):
        """Add a route definition."""
        self.routes.append(route)
        return self
    
    def add_vehicle(self, vehicle: Vehicle):
        """Add a vehicle."""
        self.vehicles.append(vehicle)
        return self
    
    def add_flow(self, flow: Flow):
        """Add a flow."""
        self.flows.append(flow)
        return self
    
    def generate_xml(self) -> ET.Element:
        """Generate complete .rou.xml content."""
        root = ET.Element("routes")
        
        # Add vehicle types
        for vtype in self.vehicle_types:
            root.append(vtype.to_xml_element())
        
        # Add routes
        for route in self.routes:
            root.append(route.to_xml_element())
        
        # Add vehicles
        for vehicle in self.vehicles:
            root.append(vehicle.to_xml_element())
        
        # Add flows
        for flow in self.flows:
            root.append(flow.to_xml_element())
        
        return root
    
    def save(self, filepath: str):
        """Save to .rou.xml file."""
        XMLGenerator.save(self.generate_xml(), filepath)
        return self


class ConfigGenerator(XMLGenerator):
    """
    Generates SUMO configuration file (.sumocfg).
    
    This is the main file that tells SUMO what files to use and how to run.
    """
    
    def __init__(self):
        self.net_file: str = ""
        self.route_files: List[str] = []
        self.additional_files: List[str] = []
        self.begin: float = 0
        self.end: float = 3600
        self.step_length: float = 1.0
        
        # Output files
        self.tripinfo_output: str = ""
        self.fcd_output: str = ""
        self.emission_output: str = ""
        self.summary_output: str = ""
        self.queue_output: str = ""
        self.statistic_output: str = ""
        
        # Processing options
        self.time_to_teleport: int = -1  # -1 = disabled
        self.ignore_route_errors: bool = True
    
    def set_network(self, net_file: str):
        """Set the network file."""
        self.net_file = net_file
        return self
    
    def add_route_file(self, route_file: str):
        """Add a route file."""
        self.route_files.append(route_file)
        return self
    
    def add_additional_file(self, add_file: str):
        """Add an additional file (detectors, etc.)."""
        self.additional_files.append(add_file)
        return self
    
    def set_time(self, begin: float, end: float, step_length: float = 1.0):
        """Set simulation time parameters."""
        self.begin = begin
        self.end = end
        self.step_length = step_length
        return self
    
    def set_outputs(self, 
                    tripinfo: str = "",
                    fcd: str = "",
                    emission: str = "",
                    summary: str = "",
                    queue: str = "",
                    statistic: str = ""):
        """Set output file paths."""
        self.tripinfo_output = tripinfo
        self.fcd_output = fcd
        self.emission_output = emission
        self.summary_output = summary
        self.queue_output = queue
        self.statistic_output = statistic
        return self
    
    def generate_xml(self) -> ET.Element:
        """Generate .sumocfg content."""
        root = ET.Element("configuration")
        
        # Input section
        input_elem = ET.SubElement(root, "input")
        
        if self.net_file:
            ET.SubElement(input_elem, "net-file").set("value", self.net_file)
        
        if self.route_files:
            ET.SubElement(input_elem, "route-files").set("value", ",".join(self.route_files))
        
        if self.additional_files:
            ET.SubElement(input_elem, "additional-files").set("value", ",".join(self.additional_files))
        
        # Time section
        time_elem = ET.SubElement(root, "time")
        ET.SubElement(time_elem, "begin").set("value", str(self.begin))
        ET.SubElement(time_elem, "end").set("value", str(self.end))
        ET.SubElement(time_elem, "step-length").set("value", str(self.step_length))
        
        # Output section
        output_elem = ET.SubElement(root, "output")
        
        if self.tripinfo_output:
            ET.SubElement(output_elem, "tripinfo-output").set("value", self.tripinfo_output)
        if self.fcd_output:
            ET.SubElement(output_elem, "fcd-output").set("value", self.fcd_output)
        if self.emission_output:
            ET.SubElement(output_elem, "emission-output").set("value", self.emission_output)
        if self.summary_output:
            ET.SubElement(output_elem, "summary-output").set("value", self.summary_output)
        if self.queue_output:
            ET.SubElement(output_elem, "queue-output").set("value", self.queue_output)
        if self.statistic_output:
            ET.SubElement(output_elem, "statistic-output").set("value", self.statistic_output)
        
        # Processing section
        processing_elem = ET.SubElement(root, "processing")
        ET.SubElement(processing_elem, "time-to-teleport").set("value", str(self.time_to_teleport))
        if self.ignore_route_errors:
            ET.SubElement(processing_elem, "ignore-route-errors").set("value", "true")
        
        return root
    
    def save(self, filepath: str):
        """Save to .sumocfg file."""
        XMLGenerator.save(self.generate_xml(), filepath)
        return self


class AdditionalGenerator(XMLGenerator):
    """
    Generates SUMO additional files (.add.xml).
    
    Contains detectors, bus stops, parking areas, etc.
    """
    
    def __init__(self):
        self.elements: List[ET.Element] = []
    
    def add_induction_loop(self, id: str, lane: str, pos: float, 
                           period: int = 60, file: str = "e1_output.xml"):
        """Add an induction loop detector (E1)."""
        elem = ET.Element("inductionLoop")
        elem.set("id", id)
        elem.set("lane", lane)
        elem.set("pos", str(pos))
        elem.set("period", str(period))
        elem.set("file", file)
        self.elements.append(elem)
        return self
    
    def add_lane_area_detector(self, id: str, lane: str, pos: float, 
                                endPos: float = -1, period: int = 60,
                                file: str = "e2_output.xml"):
        """Add a lane area detector (E2)."""
        elem = ET.Element("laneAreaDetector")
        elem.set("id", id)
        elem.set("lane", lane)
        elem.set("pos", str(pos))
        if endPos > 0:
            elem.set("endPos", str(endPos))
        elem.set("period", str(period))
        elem.set("file", file)
        self.elements.append(elem)
        return self
    
    def add_bus_stop(self, id: str, lane: str, start_pos: float, 
                     end_pos: float, name: str = ""):
        """Add a bus stop."""
        elem = ET.Element("busStop")
        elem.set("id", id)
        elem.set("lane", lane)
        elem.set("startPos", str(start_pos))
        elem.set("endPos", str(end_pos))
        if name:
            elem.set("name", name)
        self.elements.append(elem)
        return self
    
    def add_parking_area(self, id: str, lane: str, start_pos: float,
                         end_pos: float, capacity: int = 10):
        """Add a parking area."""
        elem = ET.Element("parkingArea")
        elem.set("id", id)
        elem.set("lane", lane)
        elem.set("startPos", str(start_pos))
        elem.set("endPos", str(end_pos))
        elem.set("roadsideCapacity", str(capacity))
        self.elements.append(elem)
        return self
    
    def generate_xml(self) -> ET.Element:
        """Generate .add.xml content."""
        root = ET.Element("additional")
        for elem in self.elements:
            root.append(elem)
        return root
    
    def save(self, filepath: str):
        """Save to .add.xml file."""
        XMLGenerator.save(self.generate_xml(), filepath)
        return self


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def kmh_to_ms(kmh: float) -> float:
    """Convert km/h to m/s."""
    return kmh / 3.6


def ms_to_kmh(ms: float) -> float:
    """Convert m/s to km/h."""
    return ms * 3.6


def calculate_webster_cycle(critical_ratios: List[float], 
                            lost_time: float = 4.0) -> float:
    """
    Calculate optimal cycle length using Webster's formula.
    
    C = (1.5 * L + 5) / (1 - Y)
    
    Where:
        L = total lost time per cycle
        Y = sum of critical flow ratios
    """
    Y = sum(critical_ratios)
    if Y >= 1:
        raise ValueError("Sum of critical ratios must be less than 1")
    
    return (1.5 * lost_time + 5) / (1 - Y)


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Example: Create a simple 4-way intersection
    
    # 1. Create Network
    network = NetworkGenerator()
    
    # Add center node (traffic light)
    network.add_node(Node("C", 0, 0, "traffic_light"))
    
    # Add approach nodes
    network.add_node(Node("N", 0, 100, "priority"))
    network.add_node(Node("S", 0, -100, "priority"))
    network.add_node(Node("E", 100, 0, "priority"))
    network.add_node(Node("W", -100, 0, "priority"))
    
    # Add edges (roads)
    network.add_edge(Edge("N2C", "N", "C", num_lanes=2, speed=kmh_to_ms(50)))
    network.add_edge(Edge("C2N", "C", "N", num_lanes=2, speed=kmh_to_ms(50)))
    network.add_edge(Edge("S2C", "S", "C", num_lanes=2, speed=kmh_to_ms(50)))
    network.add_edge(Edge("C2S", "C", "S", num_lanes=2, speed=kmh_to_ms(50)))
    network.add_edge(Edge("E2C", "E", "C", num_lanes=2, speed=kmh_to_ms(50)))
    network.add_edge(Edge("C2E", "C", "E", num_lanes=2, speed=kmh_to_ms(50)))
    network.add_edge(Edge("W2C", "W", "C", num_lanes=2, speed=kmh_to_ms(50)))
    network.add_edge(Edge("C2W", "C", "W", num_lanes=2, speed=kmh_to_ms(50)))
    
    # Add traffic light
    tl = TrafficLight("C", phases=[
        Phase(30, "GGGGrrrrGGGGrrrr"),  # NS through + left
        Phase(3, "yyyyrrrryyyyrrrr"),   # Yellow
        Phase(30, "rrrrGGGGrrrrGGGG"),  # EW through + left
        Phase(3, "rrrryyyyrrrryyyy"),   # Yellow
    ])
    network.add_traffic_light(tl)
    
    # Save network files
    network.save_all("./outputs", "intersection")
    
    # 2. Create Routes
    routes = RouteGenerator()
    
    # Add vehicle type
    routes.add_vehicle_type(VehicleType(
        id="car",
        length=5.0,
        max_speed=kmh_to_ms(120),
        vclass="passenger"
    ))
    
    # Add flows
    routes.add_flow(Flow("N2S", from_edge="N2C", to_edge="C2S", 
                         vtype="car", begin=0, end=3600, vehs_per_hour=500))
    routes.add_flow(Flow("S2N", from_edge="S2C", to_edge="C2N",
                         vtype="car", begin=0, end=3600, vehs_per_hour=500))
    routes.add_flow(Flow("E2W", from_edge="E2C", to_edge="C2W",
                         vtype="car", begin=0, end=3600, vehs_per_hour=400))
    routes.add_flow(Flow("W2E", from_edge="W2C", to_edge="C2E",
                         vtype="car", begin=0, end=3600, vehs_per_hour=400))
    
    routes.save("./outputs/intersection.rou.xml")
    
    # 3. Create Config
    config = ConfigGenerator()
    config.set_network("intersection.net.xml")
    config.add_route_file("intersection.rou.xml")
    config.set_time(0, 3600)
    config.set_outputs(
        tripinfo="tripinfo.xml",
        summary="summary.xml"
    )
    config.save("./outputs/intersection.sumocfg")
    
    print("✅ All files generated in ./outputs/")
    print("   - intersection.nod.xml")
    print("   - intersection.edg.xml")
    print("   - intersection.tll.xml")
    print("   - intersection.rou.xml")
    print("   - intersection.sumocfg")
