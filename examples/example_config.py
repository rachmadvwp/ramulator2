"""Example Ramulator2 configuration and simulation script"""

import ramulator

# Configure the simulation frontend that sends memory requests
frontend = ramulator.frontend.SimpleO3(
    clock_ratio=8,
    traces=["./examples/traces/example_inst.trace"],
    num_expected_insts=500000,
    translation=ramulator.translation.NoTranslation(max_addr=2147483648),
)

# Create DRAM configuration
ddr4 = ramulator.dram.DDR4(
    org_preset="DDR4_8Gb_x8",
    timing_preset="DDR4_2400R",
    rank=1,
    verbose=True,   # This prints the final timing constraints
)
# Instantiate the memory controller with the DRAM configuation
ctrl = ramulator.controller.GenericDDR(
    dram=ddr4,
    scheduler=ramulator.scheduler.FRFCFS(),
    refresh_manager=ramulator.refresh_manager.AllBank(),
    row_policy=ramulator.row_policy.Open(),
    addr_mapper=ramulator.addr_mapper.RoBaRaCoCh(),
)
# Create a memory system with the controller
mem = ramulator.memory_system.GenericDRAM(
    clock_ratio=3,
    controllers=[ctrl],
    channel_mapper=ramulator.channel_mapper.CacheLineInterleave(),
)

# Run the simulation
sim = ramulator.Simulation(frontend, mem)
sim.run()

# sim.stats returns a nested Python dict of all simulation statistics
stats = sim.stats

# Guard here for `ramulator export`, which does not run the simulation 
# but only exports the config for pure C++ Ramulator library
if stats:
    # Controller stats are under memory_system → controller
    ctrl_stats = stats["memory_system"]["controller"]

    print(f"Controller cycles:     {ctrl_stats['cycles']}")
    print(f"Avg read latency:      {ctrl_stats['avg_read_latency']:.1f} cycles")
    print(f"Read requests:         {ctrl_stats['num_read_reqs']}")
    print(f"Write requests:        {ctrl_stats['num_write_reqs']}")
    print(f"Row hits:              {ctrl_stats['row_hits']}")
    print(f"Row misses:            {ctrl_stats['row_misses']}")
    print(f"Row conflicts:         {ctrl_stats['row_conflicts']}")
    #
    print("==============================================")
    print(f"addr_mapper:                    {ctrl_stats['addr_mapper']}")
    print(f"avg_read_latency:               {ctrl_stats['avg_read_latency']}")
    print(f"cycles:                         {ctrl_stats['cycles']}")
    print(f"id:                             {ctrl_stats['num_read_reqs']}")
    print(f"impl:                           {ctrl_stats['impl']}")
    print(f"num_maintenance_reqs:           {ctrl_stats['num_maintenance_reqs']}")
    print(f"num_maintenance_reqs_served:    {ctrl_stats['num_maintenance_reqs_served']}")
    print(f"num_read_reqs:                  {ctrl_stats['num_read_reqs']}")
    print(f"num_read_reqs_forwarded:        {ctrl_stats['num_read_reqs_forwarded']}")
    print(f"num_read_reqs_served:           {ctrl_stats['num_read_reqs_served']}")
    print(f"num_write_reqs:                 {ctrl_stats['num_write_reqs']}")
    print(f"num_write_reqs_coalesced:       {ctrl_stats['num_write_reqs_coalesced']}")
    print(f"num_write_reqs_served:          {ctrl_stats['num_write_reqs_served']}")
    print(f"priority_queue_len:             {ctrl_stats['priority_queue_len']}")
    print(f"priority_queue_len_avg:         {ctrl_stats['priority_queue_len_avg']}")
    print(f"queue_len:                      {ctrl_stats['queue_len']}")
    print(f"queue_len_avg:                  {ctrl_stats['queue_len_avg']}")
    print(f"read_latency:                   {ctrl_stats['read_latency']}")
    print(f"read_queue_len:                 {ctrl_stats['read_queue_len']}")
    print(f"read_queue_len_avg:             {ctrl_stats['read_queue_len_avg']}")
    print(f"read_row_conflicts:             {ctrl_stats['read_row_conflicts']}")
    print(f"read_row_conflicts_core_0:      {ctrl_stats['read_row_conflicts_core_0']}")
    print(f"read_row_hits:                  {ctrl_stats['read_row_hits']}")
    print(f"read_row_hits_core_0:           {ctrl_stats['read_row_hits_core_0']}")
    print(f"read_row_misses:                {ctrl_stats['read_row_misses']}")
    print(f"read_row_misses_core_0:         {ctrl_stats['read_row_misses_core_0']}")
    print(f"read_throughput_MBps:           {ctrl_stats['read_throughput_MBps']}")
    print(f"refresh_manager:                {ctrl_stats['refresh_manager']}")
    print(f"row_conflicts:                  {ctrl_stats['row_conflicts']}")
    print(f"row_hits:                       {ctrl_stats['row_hits']}")
    print(f"row_misses:                     {ctrl_stats['row_misses']}")
    print(f"row_policy:                     {ctrl_stats['row_policy']}")
    print(f"scheduler:                      {ctrl_stats['scheduler']}")
    print(f"total_throughput_MBps:          {ctrl_stats['total_throughput_MBps']}")
    print(f"write_queue_len:                {ctrl_stats['write_queue_len']}")
    print(f"write_queue_len_avg:            {ctrl_stats['write_queue_len_avg']}")
    print(f"write_row_conflicts:            {ctrl_stats['write_row_conflicts']}")
    print(f"write_row_hits:                 {ctrl_stats['write_row_hits']}")
    print(f"write_row_misses:               {ctrl_stats['write_row_misses']}")
    print(f"write_throughput_MBps:          {ctrl_stats['write_throughput_MBps']}")
    #
    print(f"impl:                           {stats["memory_system"]["impl"]}")
    print(f"total_num_read_requests:        {stats["memory_system"]["total_num_read_requests"]}")
    print(f"total_num_write_requests:       {stats["memory_system"]["total_num_write_requests"]}")
    print("==============================================")
