"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
# pylint: disable-next=unused-import
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# No enable
# pylint: disable=duplicate-code,unused-argument


class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own

        self.found_closest_landing_pad = False

        self.has_set_destination = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Do something based on the report and the state of this class...

        def within(location1: location.Location, location2: location.Location) -> bool:
            radius_squared = self.acceptance_radius**2
            return (location1.location_x - location2.location_x) ** 2 + (
                location1.location_y - location2.location_y
            ) ** 2 <= radius_squared

        def euclidean_distance_squared(
            location1: location.Location, location2: location.Location
        ) -> int:
            return (location1.location_x - location2.location_x) ** 2 + (
                location1.location_y - location2.location_y
            ) ** 2

        if not self.has_set_destination:
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x, self.waypoint.location_y
            )
            self.has_set_destination = True
        elif report.status == drone_status.DroneStatus.MOVING and within(
            report.position, report.destination
        ):
            command = commands.Command.create_halt_command()
        elif not self.found_closest_landing_pad and within(report.position, report.destination):
            distance = euclidean_distance_squared(report.position, landing_pad_locations[0])
            found_location = landing_pad_locations[0]
            for i in range(1, len(landing_pad_locations)):
                new_distance = euclidean_distance_squared(report.position, landing_pad_locations[i])
                if new_distance < distance:
                    distance = new_distance
                    found_location = landing_pad_locations[i]
            command = commands.Command.create_set_relative_destination_command(
                found_location.location_x - report.position.location_x,
                found_location.location_y - report.position.location_y,
            )
            self.found_closest_landing_pad = True
        elif (
            self.found_closest_landing_pad
            and report.status == drone_status.DroneStatus.HALTED
            and within(report.position, report.destination)
        ):
            command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
