
import sys
import os

# Ensure modules directory is on path when running from project root
sys.path.insert(0, os.path.dirname(__file__))

from modules.preprocessing    import collect_input
from modules.router            import route_request, display_router_output
from modules.ann_priority      import predict_priority, display_ann_output
from modules.logic_kb          import run_logic_check, display_logic_output
from modules.csp_scheduler     import run_csp, display_csp_output
from modules.search_navigation import (run_search, display_search_output,
                                        WEIGHTED_GRAPH, UNWEIGHTED_GRAPH)
from modules.final_response    import (build_final_response,
                                        display_final_response,
                                        export_response_json)


# ────────────────────────────────────────────────────────────────────────────
#  Pipeline executor
# ────────────────────────────────────────────────────────────────────────────

def execute_pipeline(request: dict) -> dict:
    """
    Run the full AI pipeline based on the router's decision.

    Parameters:
        request (dict): Validated and standardized request object.

    Returns:
        dict: Final response object.
    """
    # ── Step 1: Request Router ───────────────────────────────────────────────
    router_output = route_request(request)
    display_router_output(router_output)

    if not router_output["valid"]:
        return {
            "request_id": request.get("request_id", ""),
            "decision":   "rejected",
            "message":    "Unknown request type. Request rejected by router.",
            "priority":   {},
            "eligibility": {},
            "assignment":  {},
            "route":       {},
        }

    ann_output    = None
    logic_output  = None
    csp_output    = None
    search_output = None

    # ── Step 2: ANN Priority (if needed) ────────────────────────────────────
    if router_output["needs_ann"]:
        print("\n[→] Running ANN Priority Module...")
        ann_output = predict_priority(request)
        display_ann_output(ann_output)

    # ── Step 3: Logic / KB (if needed) ──────────────────────────────────────
    if router_output["needs_logic"]:
        print("\n[→] Running Logic / Knowledge Base Module...")
        logic_output = run_logic_check(request)
        display_logic_output(logic_output)

        # Gatekeeper: stop here if not allowed
        if not logic_output.get("allowed", True):
            print("\n[✗] Request rejected by Logic/KB. Pipeline halted.")
            return build_final_response(request, ann_output, logic_output)

    # ── Step 4: CSP Scheduler (if needed) ───────────────────────────────────
    if router_output["needs_csp"]:
        print("\n[→] Running CSP Scheduler Module...")
        csp_output = run_csp(request)
        display_csp_output(csp_output)

        # If CSP could not schedule, stop here
        if csp_output.get("decision") == "rejected":
            print("\n[✗] CSP could not find a valid assignment. Pipeline halted.")
            return build_final_response(request, ann_output, logic_output, csp_output)

    # ── Step 5: Search & Navigation (if needed) ──────────────────────────────
    if router_output["needs_search"]:
        print("\n[→] Running Search & Navigation Module...")

        # Determine source and destination
        source = request.get("current_location", "")
        dest   = request.get("destination", "")

        # After CSP, destination might come from CSP assignment
        if not dest and csp_output:
            dest = csp_output.get("destination", "")

        if not source or not dest:
            print("  [!] Source or destination missing – skipping Search.")
        else:
            # Decide graph type (weighted for full/urgent, unweighted for simple nav)
            request_type = request.get("request_type", "")
            if request_type == "Navigation_Only":
                graph_type = "unweighted"
            else:
                graph_type = "weighted"

            # Ask if user wants comparison mode (only for Navigation_Only)
            compare_mode = False
            if request_type == "Navigation_Only":
                try:
                    choice = input(
                        "\n  Run all search algorithms for comparison? (y/n): "
                    ).strip().lower()
                    compare_mode = (choice == "y")
                except EOFError:
                    pass

            search_output = run_search(source, dest,
                                       graph_type=graph_type,
                                       compare=compare_mode)
            display_search_output(search_output, show_comparisons=compare_mode)

    # ── Step 6: Final Response ───────────────────────────────────────────────
    final_resp = build_final_response(
        request, ann_output, logic_output, csp_output, search_output
    )
    return final_resp


# ────────────────────────────────────────────────────────────────────────────
#  Main loop
# ────────────────────────────────────────────────────────────────────────────

def main():
    """
    Main entry point.
    Runs an interactive CLI loop that lets the user submit
    multiple requests until they choose to exit.
    """
    print("\n" + "=" * 60)
    print("   SMART CAMPUS AI DECISION SUPPORT & AUTOMATION SYSTEM")
    print("   AL2002 – Artificial Intelligence Lab (Spring 2026)")
    print("   NUCES – Computer Science Department")
    print("=" * 60)
    print("Type 'exit' or 'quit' as name to stop the program.\n")

    session_count = 0

    while True:
        try:
            # ── Collect structured input ─────────────────────────────────────
            request = collect_input()

            # Check exit condition (handled inside collect_input via name)
            name_check = request.get("name", "").strip().lower()
            if name_check in ("exit", "quit"):
                print("\n[★] Thank you for using Smart Campus AI. Goodbye!\n")
                break

            session_count += 1
            print(f"\n[✓] Processing Request #{session_count} "
                  f"(ID: {request['request_id']})...")

            # ── Execute pipeline ─────────────────────────────────────────────
            final_resp = execute_pipeline(request)

            # ── Display final response ───────────────────────────────────────
            display_final_response(final_resp)

            # ── Optional: save to JSON ───────────────────────────────────────
            try:
                save = input("  Save response to JSON file? (y/n): ").strip().lower()
                if save == "y":
                    filename = f"response_{final_resp['request_id']}.json"
                    export_response_json(final_resp, filename)
            except EOFError:
                pass

            # ── Continue or exit ─────────────────────────────────────────────
            try:
                cont = input("\n  Submit another request? (y/n): ").strip().lower()
                if cont != "y":
                    print("\n[★] Thank you for using Smart Campus AI. Goodbye!\n")
                    break
            except EOFError:
                break

        except KeyboardInterrupt:
            print("\n\n[!] Interrupted. Exiting Smart Campus AI.\n")
            break
        except Exception as e:
            print(f"\n[!] An unexpected error occurred: {e}")
            print("    Please try again.\n")


if __name__ == "__main__":
    main()
