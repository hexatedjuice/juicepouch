# icnd2 notes
## i. ethernet lans
### 1. implementing ethernet virtual lans
* vlan concepts 
  - definition of a lan
    1. all dev and cables in a locale
    2. all dev in same broadcast domain
  - wo vlans, s default all ports same broadcast domain
  - dotq
    * add 4by header
    * 12bi vlan id
  - intervlan routing
    * layer 3 switch
    * subintf enable router (roas)
* vlan verif
  - `show vlan brief`
  - `sh run`
  - `sh vlan id $id`
  - `show int $int switchport`
  - `sh int trunk`
* trunking (vtp)
  - cisco proprietary
  - adv vlan configs
  - disable
    * `vtp mode transparent`
    * `vtp mode off`
* voice and data vlans
  - voice vlan `switchport access vlan $id` + `switchport voice vlan $id`
### 2. stp concepts (802.1d)
* blocks ports to prevent looping
  - "broacast storms"
  - can cause mac table instability from constant looping frames 
  - can also result in fram eduplication
* does not edit direct state but adds "stp state"
* how?
  - creates "tree" of int where fwd int creates a single path from each
    ethernet link
  - spanning tree algorithm (sta)
    1. a root switch is chosen and all orts are made to fwd
    2. nonroot switches choose one port ("root port") to have smalled ad bw itself and root
       switch the cost is "root cost" 
    3. in one link, the switch w the lowest root cost is fwd; the port chosen
       is the designated port (dp)

port desc|stp state|desc
---|---|---
all root switch ports|fwd|root switch ctrls other segments
root ports on nonroot switches|fwd|least cost to reach root switch
lan designated ports|fwd|switch on each seg w lowest root cost
all other working ports|blocking|not used for fwding

* stp bridge id an dhello bpdu
  - bridge id: 8by value unique to each switch 
    * 2by priority field
    * 6by system id based on mac addr
  - bpdu (bridge pdu)
    * used to xchg info bw switches
    * hello bpdu: used to list details and ids itself
* electing root switch
  - selected based on bids recieved in bpdu
  - lowest numeric value (usually determined by the "priority" parameter)
  - all switches start as root
    * once recieving a hello w lower bid, switch over
* determining root port
  - switches add their int root cost to the cost recieved in other hello bpdus
    to calculate
* choosing dp
  - determined by comparing hello bpdu
  - tiebreaker broken w lower bpdu
* stp topology
  - default port costs

speed|<1998|2004<
---|---|---
10mbps|100|2mil
100mbps|19|200k
1gbps|4|20k
10gbps|2|2k
100gbps|n/a|200
1tbps|n/a|20

    * to enable newer version: `spanning-tree pathcost method long`
* network changes
  - hello bpdu per 2s by default
  - change detection
    1. root sends hello bpdu w cost 0 on all intf
    2. nonroot switches recieve on root ports and changes hello msg to list
       their own bpid an dfoward out dp
    3. cont until change detected
  - maxage defines how long switch waits before changing topology after hearing
    latest hello
    * everything is reevaluated
* changing int states w stp
  - roles (ex. root port, dp)
  - states (blocking/fwding)
    * can imediate fwd\>block
    * block\>fwd
      - listening phase: does not fwd frames; rm stale mac addr for which no
        frames recieved to prevent temp loops
      - learning: intf not fwd frame but mac learning begins
      - default 15s per stage
      - if was maxage, total block>fwd time = 50s (15*2+20)
* rstp (602.1w)
  - vs stp
    * same root switch, root port, dp rules and also uses blocking/fwding
    * cna be deployed in same netwk
    * higher convergence speed 
  - avoid stp timers and waiting
    * new root port mechanism wo waiting fwding state
    * new dp mech wo waiting to reach fwd state
    * lowers waiting times
  - alternate ports incase of rp failure and backup port for dp failure
* rstp states and prcs
  - rstp does not have listening state
  - admin disabled and blocking both refered to as discarding
  - rstp switches tell eo that topology has changed and directs switches to
    flush mac tables
* port types
  - p2p edge referes to connect to host
  - shared port when conenct to a hub which creates shared ethernet
    * rstp assumes al half duplex ports to be shared
* optional stp features
  - etherchannel
    * avoids convergence, adds redundancy
    * combines multiple parallel segments of equal speed bw each switch and
      treats it as one channel
  - portfast
    * allows switch to immediately transition from blocking to fwding and
      bypass listen and learn states
    * only enable of ports you know there are no bridges, switchs, or stp
      speaking devices
    * to end user dev
  - bpdu guard
    * attacker could pretend to be root switch
    * could plug into multiple ports and switches to become root and copy
      frames
    * users could innocently harm lan when they connect a switch without stp
### 3. stp implementation
* implementing stp
  - stp works without any configuration
  - default root switch usually manually config to distrib/lhigh lvl switch
  - setting stp mode
    * initially, it was one broadcast domain per vlan
    * per-vlan stp (pvstp or pvst+) gives a new stp topology per vlan
      - `spanning-tree mode pvst`
        - pvst+ is proprietary
      - `spanning-tree mode rapid-pvst`
    * there is also mst (multiple instance spanning tree) 
      - `mst`
* pvst+ is a load balancing tool 
  - creates a diff instance of stp for each vlan
  - can be used to influence assmt of rps an dps
* bridge id and sys id extension
  - priority field split into two separate fields
    * 4bi priority field
    * 12bi subfield "system id extension"
      - vlan id added
  - can only modify priority portion of bid
    * must be bw 0-65535 and a multiple of 4096 
    * `spanning-tree vlan $vlanid priority $x`
* per-vlan port costs
  - is defaulted based on ieee rules
  - can be config w `spanning-tree [vlan $id] cost $cost`
  - costs on truks affect root cost while access does not
* verifying operation
  - `show spanning-tree vlan $id`
  - `show spanning-tree root`
    * shows the root id for all vlans 
  - `show spanning-tree bridge`
    * shows bid info
* config stp port costs
  - `spanning tree [vlan $x] cost $x`
* config priority to influence root election
  - `spanning-tree vlan $id priority $value`
  - `spanning-tree vlan $id root {primary|secondary}
    * does what you think, basically auto set as root or backuo root
* optional stp feautures
  - bpduguard and portfast
    * can configure per port via int cmd
      - `spanning-tree portfast
      - `spanning-tree bpduguard enable`
    * global conf
      - `spanning-tree portfast default`
      - `spanning-tree portfast bpduguard default`
  - etherchannel
    1. add a channel group config for each int in a channel
      - `channel-group $num mode on`
    2. use same num on all intf
    * `show etherchannel $num summary`
    * dynamic etherchannels
      - PAgP (port aggregation protocol)
        * cisco proprietary
      - LACP (link aggregation ctrl protocol)
        * ieee
* implementing rstp
  - `spanning-tree mode rapid-pvst`
  - in show cmds, "discarding" mode is still rferred to as blocking
  - rstp port types

type|duplex|portfast?
---|---|---
p2p|full|no
p2p edge|full|yes
shared|half|no
shared edge|half|yes 
### 4. lan troubleshooting
* determining the root switch 
  1. get topology
  2. rule out switches w rps
  3. `show spanning-tree` will sh "this is not root" 
  4. `show spanning-tree root` will show if it is root
  5. chase the rps to root
  6. `show spanning-tree vlan $x` will tell you root switch, rp, and dp
* determining dp in segments
  1. `sh spanning-tree` cmds and look at int lists an droles
  2. id the root cost of the switch
* troubleshoot layer 2 etherchannel
  - incorrect options
    1. local switch etherchannel must have same num 
    2. channel group can differ on neighbor
    3. if using `on` you have to use it on both switches
    4. `desirable` should match w `auto` or `desirable` pagp
    5. `active` and `passive` for lacp
  - check config before adding int to etherchannel
    * speed, duplex, switchport state, access vlan, allowed vlan list
      (trunking), native vlan (trunking), stp settings
* analye switch data plane fwding
  - predicting stp impact on mac tables
* predicting etherchannel impace on mac tables
  - mac learning: frames recieved in physcial int on portchannel are considered
    to arrive on portchannel intf; mac learning adds the portchannel int
  - mac fwding: finds port channel as outgoing int when matching mac addr an
    dswitch then does load balancing on the int of the portchannel
* choosing vlan of incoming frames
  1. if port is access, associate fram e vlan id
  2. if voice port:
    1. associate frame from data device w configured access vlan
    2. asso frames from phone w voice vlan
  3. if trunk, read tagged vlan or default ot native
* troubleshooting vlans and vlan trunks
  1. id all access int and assigned vlan, correct misassigned
  2. make sure trunking vlans match
  3. check allowed vlan lists match
  4. check for incorrect config 
    * `sh vlan brief`
    * `sh vlan`
    * `sh vlan id $num`
    * `show int $int switchport`
    * `sh mac address-table`
    * vtp can remove or add vlans
### 5. vlan trunking protocol
* basic operation
  - stp will auto add added vlans to other switches
  - access switches still need to be configured 
* synchronizing the vtp database
  - switch must be configure to be vtp server or client 
  - to disable use vtp transparent
  1. for each trunk send vtp msgs and listen to recieve msgs
  2. check local vtp params vs announced vtp params
  3. if vtp params match, sync the vlan config dtabases bw the switches
* config db has revision number that increments per change
  - they sync via this rev number
  - if the rev number doesnt match it increments and adds the new data
* reqs
  - link must be is or dotq
  - vtp domains must match
  - same vtp pwd
* v2 vs v2
  - currently 3v but not covered in exam
  - v2 adds support for token rings
  - no config diff
  - transparent mode reqs that the versions of switches match
* vtp pruning
  - can cause too much flooded traffic when using vtp
  - manage broadcasts
  1. switches cna tell eachother that there is a vlan not present so flooding
     is unecessary
  2. switch will no longer flood in that port
* vtp feautures summary

funx|server|client|transparent
---|---|---|---
sends vtp msgs w isl/dotq trunks|y|y|y
allows cli vlan config|y|n|y
vlans (1-1005)|y|y|y
extended vlan(1006-4095)|n|n|y
syncs config database on recieving vtp msg|y|y|n
sends vtp msgs periodically|y|y|n
does not prcs, fwds vtp msgs|n|n|y

* vtp config
  1. `vtp mode {server|client}`
  2. `vtp domain $name`
  3. (optional) `vtp password $pwd`
  4. (optional) `vtp pruning`
  5. (optional) `vtp version {1|2}`
* vtp verif
  - `show vtp status`
  - clients show "last updater" ip as the vtp server 
* storing vtp config
  - most of it is stored in vlan.dat
  - only port config and no shutdown is in run-conf
* troubleshooting
  - no sync
    1. confirm topology
    2. id neighbor switches whose vlan db differ w `show vlan`
    3. on neighbor switch verif:
      1. it is trunking
      2. same domain name
      3. same pwd
      4. md5 digest same
  - problems when adding switches to netwk
    * may not match topology configs
### 6. misc lan topics 
* securing access w ieee 802.1x
  - need to ensure security
  - usr/pwd
  - eap and radius protocol
* aaa authentication
  - external aaa server
  - login prcs
    * access ctl server (acs) is aaa software
    * define tacacs+ (tcp) or radius (udp) protocol

deatures|tacacs+|radius
---|---|---
most often used for|netwk dev|usrs
transport|tcp|udp
auth port|49|1645,1812
encrypt pwd|y|y
encrypts whole packet|y|n
funx to auth user to subset of cli cmds|y|n
defined by|cisco|rfc 2865

* config examples
  - `aaa new-model` nables aaa service for local dev
  - config server
    * `tacas server $name`
      - `address ipv4 $addr`
      - `key $key`
      - `port $port`
  - group servers
    * `aaa group server $name`
      - `server name $name`
  - enable logon: `aaa authentication default $method1 $method2`
    * ex. `aaa authentication default group WO-AAA-Group {local|login}`
      - local uses locla users and login uses login pwd
* dhcp snooping
  - can be mim by masking as a dhcp server and setting own ip at default
    gateway
  - dhcp snooping filters out any sus msgs that may be an attacks
    * can filter offer and ack requests on untrusted ports
    * also remebers addrs and macs in dhcp binding table
  - apply more cplx logic for untrested client ports 
  - rate limiting
* switch stacking 
  - allows engineers to stack switches to act like one switch
  - one mgmt ip address, one config file, stp/cdp/vtp runs on one switch,
    switch ports appear to be the same switch, one mac addr table for all ports
  - stacking ports (cisco flexstack)
    * flexstack plus also (2013)

attrib|flexstack|plus
---|---|---
yr|2010|2013
models|2960s,2960x|2960x,2960xr
speed (full duplex)|10gbps|20gbps
min switches|4|8

  - form a loop xrs all stacked switches
  - simplifies scope of operations
* chassis aggregation
  - meant for more pwrful switchs (distrib and core)
    * no special adapters, ether intf
    * aggs 2 switches
    * cplx but more funx
  - connection w etherchannel bw switches
  - mec (multichasis etherchannel): can be config bw 2 phys switches
    * ex. cnxn of access switches to aggregated distrib switches
  - active/standby ctl plane: simpler operation for ctl plane bc pair acts as
    one switch (ie. stp, cdp, tc.)
  - active/active data plane: can sync mac tables for fwding
  - single switch mgmt: simpler operation of mgmt protocols bc sync w other
    switch
## ii. ipv4 routing protocols
### 7. understanding ospf concepts
* interior and exterior routing protocols 
  - igp: designed and intended for use inside a single autonomous sys (as)
  - egp: designed for use bw as
    * today only bgp is still in use
  - as: a ntwk ctrl under single org 
  - comparing igps
    * usually use eigrp or ospf
    * types: linkstate, distance vector, advanced distance vector (balanced
      hybrid)
  - metrics
    * ripv2: hop ct
    * ospf: cost (based on bandwidth)
    * eigrp: composite delay+bandwidth (based on slowest link + cumulative
      delay)
    * infinity as 2^24 -1
* ad table

route type|ad
---|---
conected|0
static|0
bgp(external)|20
eigrp(internal)|90
igrp|100
ospf|110
isis|115
rip|120
eigrp(external)|170
bgp(internal)|200
dhcp|254
unusable|255

* ospf concepts and operation
  - exchg data link state adv (lsa) 
  - data is flooded to every router
    * def per30min
  - organizes lsas in lsdb (link state db)
    * `sh ip ospf database`
  - dijkstra spf
    1. become neighbors (share datalink)
    2. xch db
    3. add best routes
* ospf neighbors
  - est by sending hello msgs auto
    * `sh ip ospf neighbors`
  - allows for dynamic discovery
  - contains rids of each
    * calc based on active int v4 addr
  - neighbors if same subnet
  - ospfy header: protcol type 89
    * sent to 224.0.0.5 multicast for ospf
    1. \>seen[], rid 1.1.1.1
    2. \<seen[1.1.1.1], rid 2.2.2.2
    3. \>seen[1.1.1.1,2.2.2.2], rid 1.1.1.1
* xchg lsdb bw neighbors
  1. list is sent to check if there are repeats
  2. query for missing lsas sent
  3. lsu (link state update) pkgs are sent w multiple lsas
* maintainance of neighbor and lsdb
  - monitos rs w hello and dead intervals
    * if neighbor is silent for dead intv, considered failed (default 4x hello)
  - when considered failed, new lsas are also flooded
  - when no changes, flood every 30min
* designated routers on ether links
  - ospf selects one to be dr and backup dr
  - xchg bw dr and all other rs to minimize msg flow
    * bdr watches status to ensure it can take over on failure
  - 2way: "adjacent" - neighbor sent a hello that lists r rid and all checks
    are passed
  - full: "fully adjacent" - both rs know same lsdb info and have completed
    lsdb xchg
 * ospf area design
  - usually routing works with all rs assigned so same area (def 0)
  - falls apart with larger netwks
    * reqs more mem and prcs pwr, longer convergence
  - areas
    * same subnet, contiguous, internal rs all intf to that area, abr routers,
      backbone to same area
  - how areas reduce calc time
    * only brief summary info abt nonarea sections
### 8. implementing ospf for ipv4
* single area ospfv2
  1. `router ospf` 
  2. (optional) config ospf router id
    1. `router-id $value`
    2. `interface loopback $num` and `ip address $addr $mask` to config an ip
       addr on a loopback int 
  3. use 1+ `network $num $wildcard area $id` cmds to enable ospfv2 on int
     match w config ip and mask 
  4. (optional) use `passive-interface $int` to config on access lines/no
     neighbors
  - indirect int assignment
  - ntwk matching w wildcards
* verif single area ospf
  - `show ip ospf`
    * `... neighbor` also shows local int, neighbor id, state, and addr
  - `sh ip ospf database`
  - `sh ip route`
  - `sh ip protocols`
    * shows rid and minor info
  - `sh ip ospf int brief`
    * shows interface, pid, addr, cost, state
* multiarea ospfv2
  - only abrs have multiple areas config
    * imlicitly config by assigning multiple int
  - verification
    * config
      - `sh run`
    * enabled int
      - `sh ip ospf int`
      - `... $int`
      - `... brief`
    * neighbors
      - `sh ip ospf neighbor`
      - `... $int`
    * lsdb config
      - `sh ip ospf database`
    * routes 
      - `sh ip route`
      - `... ospf`
      - `$int`
      - `| section $subnet`
* verif dr and bdr
  - `sh ip ospf int $int`
    * gives you bdr and dr addr and rid
    * can be found by tracing neighbors
* additional ospf features
  - default routes
    * can advertise default route w `default-information originate`
  - ospf metrics
    * based on bandwidth
    * reference bandwidth / int bandwidth
      - reference can be set
    * can be toggled by changing bandwidth
    * bc lowest ospf cost is 1, problems w higher bandwidth
      - fix w `auto-cost efernce-bandwidth $speed`
  - ospf load balancing
    * set i `maximum-paths $num`
  - int config
    * can be specified by specifying netwk of the int
### 9. understanding eigrp concepts
* uses bandwith and delay metrics
* higher convergence
* partial update msgs and split horizon to minimize load
* route poisoning
  - failed routes are removed and are advertised as an infinite metric
  - rip uses 16
  - eigrp uses 2^32 -1
* partial updates
  - sends info abt each route once and only does partial updates after
  - no update if no change lol
* hello neighbor status
  - bc no periodic updates > periodic hello msgs
  - wo hello, assumes failed
* eigrp msgs to 224.0.0.10
* concepts and operation
  - neighbor discovery: uses hello
  - topology updates: only once w first contact, then partial w topology
    changes
* egrp neighbors
  - must use same auth, same config autonomous sys num, src ip must be wi same
    subnet, k-values match
  - no interim states
  - updates done w rtp (reliable transport protocol)
    - mechanism for fault tolerance
* metric calculation
  - m = (10^7/least bandwidth + cumulative delay) * 256
    * where least bandwidth is lowest bandwidth link in route using kbps
    * cumulative delay is sum of all delay values for all outgoing int in the
      route w unit tens of microseconds
  - caveats on bandwidth on serial links
    * serial links default to 1544 bandwidth and 20000microsec delay
* convergence
  - feasible distance (fd): local router composite metric of best route to
    a subnet
  - reported distance (rd): next hop router's composite for the same subnet
  1. one router calculates fd and sends info used to calculate to next router
  2. that router then uses that info to calculate its own fd 
  - successors and feasible successors 
    * the route w best metric to a subnet is the successor
    * the backup is the feasible
      - a nonsuccessor route is the backup if the rd is less than the fd
  - thus convergence is pretty fast
  - when a route fails wo backup, dual (diffusing update algorithm) is used
    * sends queries to look for loop free route to subnet
    * confirms that route exists and replaces the failed w new alt route
### 10. implementing eigrp for ipv4
* core eigrp config
  1. `router eigrp $asn`
  2. config ntwks `network $ip $wildcard` to enable intf w matching ips
  3. (optional) `eigrp router-id $num` to set rid
  4. (optional) `ip hello-interval|hold-time eigrp $asn $time`
  5. (optional) `bandwidth $num` and `delay $num` to toggle metrics
  6. (options) `maximum-paths $num` and `variance $multiplier` to support for
     equal cost routes
  7. (optional) `auto-summary` 
  - routers with different asns will not become neighbors
* verifying core features
  - config 
    * `sh run`
  - enabled int
    * `sh ip eigrp interfaces`
    * `... detail`
    * `... $int`
    * `sh ip protocols`
  - neighbors
    * `sh ip eigrp neighbors`
    * `... $int`
    * `sh ip protocols`
  - topology
    * `sh ip eigrp topology`
    * `... $subnet/prefix`
    * `... | section $subnet`
  - routes
    * `sh ip route`
    * `... eigrp`
    * `... $subnet $mask`
    * `... |section $subnet`
* metrics, successors, and feasible successors
  - viewing eigrp topology table
    * will show successors and such
    * finding feasible successors
      - list the verbose output to show all possible routes, fs can be seen by
        the metric not matching the fd of the successor and the rd of the fs
has to be less than that of that metric  
* other eigrp config settings
  - load balancing
    * there is unequal load balancing which allows routes w similar but not
      identical metrics to be treated as such
      - determined by "variance" variable
      - multiplied by fd of each route
      - non fs or s routes cannot be added for fear of creating a loop
  - autosumm and discontiguous classful ntwk
    * problems arise w autosumm when discontiguous
    * can be toggled `no autosummary`
* eigrp symbolized w "D" in routing table
### 11. troubleshooting ipv4 routing protocols
1. examine interntwk design to determine which int routing protocol runs on and
   which should be neighbors
2. verify whether routing protocol enabled on each int
3. verify each router formed all expected neighbors
* int enabled w routing protcol
  - `sh ip eigrp int` shows enabled int excluding passive
  - `sh ip ospf int br` shows enabled and passive
  - `sh ip protocols` shows netwk config cmds and passive int
* neighbor relationships

req|eigrp|ospf
---|---|---
up/up|y|y
same subnet|y|y
acl does not filter routing msgs|y|y
pass auth|y|y
same asn/pid on `router` config|y|n
hello/hold timers match|n|y
rid unique|n|y
kvalues match|y|n/a
same area|n/a|y

  - eigrp debug
    * `debug eigrp packets`
    * `sh ip protocols`
  - ospf debug
    * `debug ip ospf hello`
    * mtu mismatch can also stop neighbor form    
## 12. implementing external bgp
* bgp concepts
  - only egp used today
  - focus on reachability: learning abt subnets and calc route for subnets 
  - advertise w update messages to neighbors
  - can be used to adv pub ip to isp
* internal v external
  - ebgp used to adv route bw diff asn
  - ibgp used to adv route wi asn
* choosing routes
  - instead of metrics use "path attributes"
    * each prefix adv along w a list of path attrib
  - uses as\_path path attribute (pa) in one step of the slection
    * smaller one would be selected as being "better"
* egp and internet edge
  - single homed: one link to isp
    * any kind of wan link, that is dsl, mpls, etc
  - dual homed: two links to one isp
  - multihomed: multiple isps
* advertising public enterprise prefix into internet
  - only adv public nat addr
* learn default routes from isps
  - can be learned w ebgp
  - makes more sense than dynamic to avoid next-hop learning
    * too many routers
  - isp share ip to ebgp routers of enterprises
  - to make use of this route, the enterprise router can adertise the this
    default router in internal ntwk 
    * for ospf can be config w `default-information originate`
* config
  - predefine neighbors w `neighbor $addr remote-as $asn` subcmd
  - adv abt prefixes that have been added to the bgp table using:
    * `network`
    * route redistrib
    * learning from neightbor
  - uses tcp transport port 179
    * becomes neighbors after checks passed
    * update msgs used to xch info w prefix/length (network layer reachability
      info or nlri) and path attribs 
  1. proper config results in peer formation
  2. addition config like `network` resukts in route being added in local bgp
  3. ebgp adv all bets possible routes in table in an update msg
  4. bgp recieves on other router, adding route to table
  - config intiated w `router bgp $asn`
* verif
  - `sh ip bgp summary` lists one line per bgp peer

peer state|reason
---|---
idle|admin down or waiting for next retry
connect|tcp conn attempted but not complete
active|tcp complete but not bgp msgs sent
opensent|tcp active and first msgs sent to estab peer
openconfirm|tcp active and recieved first msg to est peer
established|peer made

  - neighbors diabled w `neighbor $ip shutdown`
  - dmzs and subnets can be advertised much the same way
    * however, isp does not need subnet routing info, but the router itself
      cannot see its full path
      - use discard route or `network $publicipdomain maks $mask` would not
        register
      - can be given to the int null0
## iii. wans
### 13. implementing p2p wans
* leased line wans with hdlc
  - full duplex
  - hdlc: high lvl datalink ctrl
  - csu/dsu (channel/data serive unit0: performs clocking and sits bw company
    ntwk and telco wan
    * connect w wics (wan int crads) or nims (netwk int module)
* hdlc 
  - cisco propr.
  - perform simple p2p topology funx
  - has a fcs
  - encapsulates an ip packet after stripping 802.3 header
  - config
    1. `ip address $addr $mask` 
    2. use only when conditions are true:
      1. if `encapsulation $prtcl` already exists, use `encapsulation hdlc` to
         enable hdlc or disable previous `encapsulation` cmd
      2. `no shutdown` if admin down
      3. `clock rate $speed` to config clocking rate, only do this on dce cable
    3. optional
      1. `bandwidth $speed` (in kbps) to match clock rate of link
      2. `description $text`
* leased lines wans w ppp
  - point to point protocol
    * non proprietary
    * defines header and trailer
    * support both sync an dasync links
    * type filef in header to allow layer 3 over same link
    * pap and chap built in
      - plain text pap
      - challeneg handshake is much more secure
        * hashed  
    * ctrl protocol allows higher lvl to ride over ppp
      - link control protocol (lcp): focuses on datalink
      - netwk ctrl protocol (ncp): one per network layer protcol; funx specific
        to related layer 3 protcol
    * features

funx|lcp|desc
---|---|---
looped link detection|magic number|detects loops and disables int
error detection|link qual monitoring (lqm)|disables int that exceeds error cap
multilink support|multilink ppp|load balancing
auth|pap and chap|xch names and pwd to verif

    * implementation 
      - `encapsulation ppp`
      - chap
        * define host name
        * `username $user password $pwd` 
        * `ppp authentication chap`
      - pap
        * `authentication ppp pap`
        * `ppp pap sent-username`
  - multilink
    * load balancing
    1. config matching multilink int on routers 
    2. config serial int an dauthentication
    3. config ppp cmds on both multilink and serial int to enable mlppp and
       asso multilink w serial int
      - `interface multilink $num`
    * can be shown in `sh ip route`
* troubleshooting 

line stat|prtcl stat|likely reason
---|---|---
admin down|down|int shutdown
down|down|layer 1
up|down|layer 2
up|up|layer 3

  1. ping attempt
  2. if fails, examine int stat
  3. if ping works, verify routing protocols are xching routes
  - layer 2 pblms
    * down both ends: mismatch encapsulation
    * down on one: keepalive disabled on the end in the upstate when using hdlc
    * down both: pap/chap failure
  - keepalive failure
    * helps notice when link is nonfunx
    * brings down link if nonwork
  - auth fail
    * `debug ppp authentication`
      - o is output (has sent chllg), i is input (has recieved response), o failure sent a failure msg  
### 14. private wans w ethernet and mpls
* metro ethernet
  - includes variety of wan services w common features
  - acts as if wan service were created by one ethernet switch
  - each customer is provided an ethernet access link
  - services and topologies

service|short name|topology terms|desc
---|---|---|---
ethernet line|e-line|p to p|two cpe xchg frames (like leased lines)
ethernet lan|elan|full mesh|acts like lan
ethernet tree|etree|hub and spoke;partial mesh| central comm to remote sites

* eline
  - connects two sides w access links thru evc (ethernet virt circuit)
  - routers use phys ethernet int, routers would config ip in same subnet as
    other, routing protocols becomes neighbors and xchg routes
  - each route in a diff subnet
* elan (full mesh)
  - full mesh topology
  - contained wi one subnet
  - rss intensive
* tree (hub and spoke)
  - "leaves" can only send to main branch which then fwds
  - one subnet per evc
* ethernet virtual circuit bandwidth profiles
  - access links transmit at a predefined speed
  - some may want an arbitrary rate that is not a standard, this can be fixed
    with a bandwidth profile w cir (commited info rate)
  - ctrl overage wpolicing and shaping
    * shaping tells routers to slow down
    * alternatively, frames can be discarded if over limit
* multiprtcl label switching (mpls)
  - allows sp to connect to multiple users and keep traffic separated
  - uses lable switching
  - creates a layer 3 vpn essentially
    * allows for obfuscation bw origination bw netwks
    * customer and provider edge
  - quality of service
    * does not discriminate per packet type wo qos
    * qos gives packets like voip bette treatment
  - aware of customer addressing
  - ce routers learn routes from other routers
    * through prcs called route redistrib
  - ospf area design w mpls vpn
    * usually distrib cluster treated as backbone
  - eigrp challenges
    * assign ce routers to different asns   
### 15. private wans w internet vpn
* internet access
  - digital suscriber line: internet provided thru tel line
  - cable internet: internet thru same as tv line
    * catv instead of tel cabling
  - wireless wan (3g,4g,lte): mobile phone etc  thru radio waves
    * lte is long term evolution part of 4g tech
  - fiber
    * most cabling implements copper usage
    * allows for faster internet
* vpn fundamentals
  - confidentiality: prevent mim attacks
  - auth: ensure valid sender
  - integrity: msgs get through wo alteration
  - antireplay: preventing mim to copy and spoof later packets
  - vpn tunnel used
    * vpn headers added to packet
* site to site vpns with ipsec
  - ipsec: architechture/framework to define sec services for ip prtcls
    * encrypts data w formulas in a matched set
      - one to encrypt, one to decrypt
* ssl support
  - alternative to ipsec
  - dynamic creation of secure sessions
  - port 443
* gre tunnels
  - generic routing encap
  - treated like a p2p connection
  - virt int treated as tunnels
  - over the unsecured internet
    * create int `int tunnel $num`
    * delivery header and gre header added onto og packet
    * no encryption, just encapsulation
      - encryot can be added
  1. `int tunnel $num`
  2. (optional) `tunnel mode gre ip` to use encapsulation
  3. `ip address $addr $mask` the two routers should be on the same subnet
  4. config sunnel src ip addr in unsecured part of netwk, local src ip must
     match the other routers dest ip
    1. `tunnel source $addr`
    2. `tunnel src $int` also sets it via interface
  5. `tunnel destination {$addr|$hn}`
  6. add routes that use the tunnel by enabling a dynamic protcol or via static
     config
  - verif
    * `sh ip int br` shows it listed as a tun int
  - troubleshooting
    * check src and dest matching and correctness
  - acl and security issues
    * have a permit ip to match the unsecured public ip or have a permit gre
      which matches the protcol and public ip
    * `permit gre any any`
* dmvpn
  - using mult gre tunnels issues
    * static route config
    * extra config
    * more overhead and prcsing
  - facilitates sending and rec to and from any site on channel
  - instead of p2p, uses dynamic next hop resolution protocol (nhrp) 
    1. one site acts as a nhrp server and hub
    2. spokes can initially only connect to hub
    3. spkes (nhrp clients) register pub and priv addr w nhrp servers to
       initiate routing
  - when a client registers, it adds its public and priv (tunnel) ips to
    a table which it then shares with the other clients
* ppp over ethernet
  - used for ability to assign ips to other end of the link
  - initially used in dsl but needed to switch to internet methods
    * encapsulation of ppp wi ip packets
  - config 
    * dialer int are logical int that can be dynamically linked to use another
      int
    * add int into groups w `pppoe-client dial-pool-number $num`
    * can refer to other dialer int w `dialer-pool $num`
    * configure `encapsulation ppp`
    1. config a dialer int:
      1. `int dialer $num` to create
      2. `dialer-pool $num to refer to a pool of ethernet int that can be used
         for pppoe`
      3. `pppoe-client dial-pool-number $num` on each phys int to add int into
         same pool configured on dialer int
    2. configure ppp on dialer int
      1. `encapsulation ppp`
      2. `ppp chap hostname $name`
      3. `ppp chap password $pwd`
    3. configure ip routing
      1. `ip address negotiated` to tell dialer to use ppp's ipcp to learn
      2. `mtu 1492` ti change from default to allow for extra 8by pppoe header
      3. `no ip address` to disable ip routing on phys int and remove v4 addr
         from routing table
  - verif
    * show in `sh int dialer $num`
    * `sh run`
    * `sh ppoe session`
## iv. ipv4 services: acls and qos
### 16. basic v4 acl
* types
  - standard 1-99
  - extd 100-199
  - addiitional: standard 1300-1999 ext 2000-2699
  - named
* `access-list {1-99|1300-1999} {permit|deny} $params
* deploy w `ip access-group $num {in|out}
### 17. adv v4 acl
* `access-list $num {deny|permit} $prtcl $src $srcwildcard $dest $dstwildc
  [eq $port] [established] [log]`
* acl editing
  - via seq numbers 
  - delete indiv lines w `no $linenum`
  - add lines w a seq num before the cmd written
* `sh ip access-lists` and `sh access-lists` show line numbers and conf
### 18. quality of service
* manage bandwidth, delay, jitter, loss
* data, video, and voice packets are managed
* classification and marking
  - allows for prioritization and separation
  - cpx matching then goes to marking for the packet to be fwded
  - matching can be done w acls or network based app recog (nbar) by cisco
  - marking is performed w a tos (type of service byte) in ip header
    * used to be ip precedence (ipp), now is dscp (differentiated srv code pt)
      which increased capacity
  - marking ethernet frames
    * also has a type field w a cos/pcp (class of service/priority code pt) 

field name|headers|length|where
---|---|---|---
dscp|v4,v6|6|end to end packet
ipp|v4,v6|3|end to end packet
cos|802.1q|3|vlan trunk
tid|802.11|3|wifi
exp|mpls|3|mpls wan

  - trust boundaries
    * pt in path where devices can trust qos marking
    * switches and ip phones can be use to detect markings
* diffserv rfc suggested marking values
  - expedited fwding (ef): used to mark voice payloads, other high priority
  - assured fwding (af): defines 12 values that are used together; defines
    3 lvls of drop priority and 4 lvls of queue   
    * follow afxy 
      - where x is the queue (1 worst, 4 best)
      - y is drop priority (best drop 1, worst drop 3)
  - class selector (cs): w dscp there is 8 bits
      - first 3 reserved for ipp for backwards compat
* congestion mgmt (queuing)
  - mg packets while waiting to exit int or waiting for rss
  - can be simple like fifo 
  - roud robin, cycles through all queues 
    * can also be weighted
  - low latency queuing (llq)
    * has less delay than round robin so better for voice an dvideo packets
    * one queue is always "next" any packets thru there are fwded first
    * call admission ctrl (cac) can help police to make sure not too many voice
      and video that floods
* shaping and policing
  - both monitor overall bit rate
  - policing drops packets to match specified rate an dshapers hold a queue
  - makes sur ecustomers dont use above cir 
  - shaping must allow voice and video packets thru wo too mcuh delay
    * thus use 10ms interval hold
* congestion avoidance
  - to avoid tail drops in queuing where overflow packets in queue are dropped
  - tcp windowing
  - you can use tool to do %drops in the queue to prevent it form maxing out
  - mgmt mostly concerned w tcp bc it takes the longest, needing a confirmation
    response
    * voice and video use udp
## v. v4 routing and troubleshooting
### 19. ipv4 rouitng in the lan
* troubleshooting roas
  1. check encapsulation
  2. chekc vlan ids and trunking stats
  3. check roas subint config
  4. native vlan match
* vlan routing w layer 3 svis
  - applicable on layer 3 switches
  1. enable ip routing on switch
    1. `sdm prefer lanbase-routing` to change switch to asic (app specific
       integrate circuit) settings to make
       space for v4 routes on reload
    2. `reload` and switch to new `sdm prefer` setting
    3. `ip routing` to enable v4 routing
  2. config svi int (one per vlan)
    1. `interface vlan $vlanid`
    2. `ip address $adrr $mask` in vlan int config mode to put ip addr and mask
       on vlan int
    3. `no shutdown`
  - verif w `sh ip route`
* vlan routing w layer 3 switch routed ports
  - svis act only if the dst for a packet is a mac address of the switch itself
    * otherwize they are ethernet int
  - can be made to act like phys int
    * ethernet frame is stripped and a layer 3 fwding decision is made then
      ethernet frame reattached and fwded in its new frame
  - use `no switchport` on rh physcial interface 
    * layer 3 capable switches alwys are preconfigured w `switchport` on int
* layer 3 etherchannels
  1. config phys int
    1. `channel-group $num mode` to add int to channel
    2. `no switchport` to make phys port routed ports
  2. config portchannel int
    1. `interface port-channel $num`
    2. `no switchport` to make it act routed
    3. `ip address $addr $mask`
  - verify
    * `sh etherchannel $num summary` 
    * `sh ip route`
  - troubleshooting
    * must be `no switchport`
    * speed and duplex must match
### 20. implementing hsrp for first hop routing
* fhrp 
  - first hop redundancy prtcl
    * routers appear to be one router w no user intervention
    * if one fails, fhrp decides to use the other
  - ntwks need to have redundancy
    * single pts of failure are the weakest

name|origin|approach|load balancing
---|---|---|---
hot standby router protcol (hsrp)|cisco|active/standby|persubnet
virtual router redundancy prtcl (vrrp)|rfc 5798|active/standby|persubnet
gateway load balancing prtcl (glbp)|cisco|active/active|per host

* hsrp
  - active/standby (or passive)
  - allows 2+ routers to coop
    * at any one time, only one router is the default
  - active router uses virtual ip addr and matching virtual macs
  - failover
    * moves the virtual mac an dip over to another router
  - load balancing
    * supported by prefering diff router based on subnet
* implementing hsrp
  - `sh standby brief` shows int, group, priority, state, virt ip
  - priority
    1. discover no other hsrp router in subnet, become active router
    2. discover existing and negotiate, highest priority is winner
    3. discover existing hsrp and already active
      1. if `no standby preempt` then become standby
      2. if `standby preempt` then contest the active router
  * change ver w `standby version {1|2}`
    - v2 has v6 support, milisec hello timer, greater group num range, and uses
      a unique id for each router
    - mac addr and multicast used 
      * v1: 0000.0c07.acxx, 224.0.0.2
      * v2. 0000.0c9f.fxxx, 224.0.0.102
* troubleshooting
  - must be same ver, same virtip wi same subnet and not being used, attached
    layer 2 switches in same vlan, no acl filtering
### 21. toubleshooting v4 routing
* based on host settings
  1. check dns server addr
  2. check host default gateway 
  3. check subnet
* dhcp issues
  1. make sure `ip helper-address` is config
  2. make sure dhcp server is config
## vi. ipv6
### 22. v6 routing operation and troubleshooting
* quick review facts
  - 128bit addr
  - dhcp v6 uses ndp for default gareway
  - slaac can also give addr auto
  - v6 routing enabled w `ipv6 unicast-routing`
* troubleshooting
  - host issues
    * same v6 subnet as router
    * same prefix as router
    * default gateway w router's real addr
    * correct dns addr
  - router issues
    * up/up int state
    * same datalink routers should be in same subnet
    * should havee routes to all v6 subnets per design
  - filtering
    * watch for mac address filtering on lan switches
    * watch for missing vlans
    * acl lists
* stateless slaac
  - can be used for stateless dhcp wo a server
### 23. implementing ospf for v6
* ospfv3
  - added support for v4 w "addr families"
    * for dual stack
  - also uses lsas but some definitions have changed and new lsas added
  - "o" means ospf and "oi" means ospf interarea route
    * ad/cost
* config
  1. `ipv6 router ospf $prcsid`
  2. config rid
    1. `router-id $id`
    2. config v4 addr on loopback int 
    3. relying on v4 int choose highest v4 addr 
  3. `ipv6 ospf $prcsid $area $area` per int
  4. (optional) `passive-interface $int`
* other ospfv3 config
  - can toggle cost etc
  - load balancing
  - default routes
* verification and troubleshooting
  - basically all cmds but ip becomes ipv6
  - in v3, int dont have to be in the same subnet to become neighbors
* v6 mtu issues
  - mtu mismatch will cause neighbor formations to fail
  - can change v6 to 1400 instead of default 1500
### 24. implementing eigrp for v6
* to enable on an int use `ipv6 eigrp $asn` in interface subcmd mode
* theres no autosumm for v6 eigrp
* interfaces do not have to be in the same subnet to be neighbors
* other config like hello timers are config the same except under v6
### 25. v6 acls
* basics
  - can only match v6 packets
  - v6 only use names 
  - match v6 header specific details
  - have implicit permit before final deny all
  - beware of filtering
    * ndp an dpmtud (path mtu discovery) msgs cannot be filterd
* capabilities
  - traffic class
  - flow label
  - v6 next header field w extension header
  - src and dst addr
  - tcp/udp 
  - icmpv6 type and code
* limitations
  - tunneled traffic is difficult to filter
  - prefix lengths must be divisible by 4
* config
  - wildcard indicated by prefix header
  - operator port-number 
  - extended
    * can match icmp messages
* implicit acl rules
  - there is a `deny ipv6 any any` at the end as always
  - make sure not to filter essential packets
  - v6 mgmt ctrl acls
    * access class can be employed like in v4
  - can apply both v4 and v6 applied in and outbound on a single int
  - the implicit allow allows ns and na advertisements for slaac and v6
## vii. misc
### 26. ntwk mgmt
* simple ntwk mgmt prtcl (snmp)
  - each agent has mgmt info base (mib)
    * stores config vars
    * can be polled by manager
      - thru get req
    * can also set var by nms
      - thru set req
  - trap and inform msgs
    * same purpose diff mechanisms
    * inform adds reliability, needs an acknowledgement or will resend
    * both tell manager of events
* secure snmp
  - use acls to filter unknown snmps
  - only host to send legit is the nms
  - v1
    * both config w a "community string" 
    * if req sends correct string, agent will respond
  - v2c
    * "version 2 community"
    * basically the same as v1
  - v3 
    * implementation of integrity, auth, and encryption
    * much more modern sec
* implementing v2c
  - config for get and set req
    1. `snmp-server community $string RO [ipv6 $acl] [$acl]`to enable snmp and
       restrict incoming snmp msgs to acl and set read-only
    2. (optional) `snmp-server community $string RW [ipv6 $acl] [$acl]` for read
       write privs
    3. (optional) if you did use an acl, config it
    4. (optional) `snmp-server location $desc` 
    5. `snmp-server contact $name`
  - config trap and inform req
    1. `snmp-server host {$hostname|$addr} [informs] version 2c
       $notifcommunity` to send traps (default) or informs to host
    2. `snmp-server enable traps` to enable sending of all trap and inform msgs
  - verif
    * `sh snmp community`: gives community string values
    * `sh snmp host`: lists ip addr or hostname of nms referenced
    * `sh snmp`: focus on status na dcounter info
* implementing v3
  - v3 groups
    * each `snmp-user` refers to a `snmp-server group` for easier config
    * groups can share a pwd
    * `snmp-server group $name v3 {noauth|auth|priv} [write $viewname] [access
      [ipv6] $acl]`
      * only priv encrypts msgs
  - `snmp-server user` configs user, auth pwd, pwd hash alg, encryption key,
    encryption alg, and `snmp-server group` 
  - config summary
    1. `snmp-server group $name v3 {noauth|auth|priv} [write v1default] [access
       [ipv6] $acl` to enable snmp agent
    2. to config "noauth" users `snmp-server user $name $grp v3`
    3. for "auth" users
      1. `snmp-server user $name $grp v3 auth {md5|sha} $pwd`
    4. for "priv" users
      1. `prive des $encrypkey` params at the end of user cmd or diff encryp
         algor
        * aes can be config w 128, 192, 256 
    5. enable agent to sen dnotifications
      1. `snmp-server host ...` 
      2. enable traps
* ip service lvl agreement (sla)
  - provides means to measure and display several key perf and availability
    indicators
  - can be used to mimic user traffic without hardware implements
  - analyzation of flow data
    * `sh ip sla statistics $num`
* span (switched port analyzer)
  - concepts
    * the ntwk interface card (nic) 
    * can be run on a vm
  - tx: transmitted out a port frames
  - rx: recieved frames of a port
  - redirects frames out another port so that pgms like wireshark can analyze
* span session
  - it can also copy frames being sent through
* configuring local span
  - each span dst port can only support 1 session at a time
  - dst ports can also be src ports
  - span ports not treated as normal port
  - can be moved from one monitor session to another
  - multiple span srcs can be made into single session
  - session cannot mix intf and vlan srcs
  - trunks can be src ports
  - etherchannel int can be used as src
  1. `monitor session $num sourceninterface $int [- last-in-range]
     [rx|tx|both]` to define a span session by number an ddefine one src int,
repeat for all src ports
  2. `monitor session $num source vlan $vlan [rx|tx|both]` to id a span session
     by number and add a src vlan, repeat per vlan src
  3. `monitor session $num destination interface $int` to define one dest port
     for monitor session
* verif
  - `sh monitor session all`
  - `sh monitor detail` specific
  - `sh monitor session` lists src ports and vlan  but breaks down info based
    on ports  
* limiting span srcs
  - minimize traffic capture
### 27. cloud computing
* server virtuzlization
  - can virtuzlize sevrers
* cisco hardware
  - no kvm (key, video, mouse)
  - racka of servers in data center: not to waste space
* virtualization is managed under a hypervizor within a single phys machine
  - vmware vcenter
  - mc hyperv
  - citrix xenserver
  - redhat kvm
* virtual switch wi system that connect to vnic of each vm
* each host cable to top of rack (tor) switches which is then linked to end of
  row (eor) switchs
* engineers can use api to config/mv/add/del vms to meet needs vs removing
  physical hosts
  - os is decoupled so it can run on any server w enough rss
* cloud computing service requirements
  - on demand self-service: consumer chooses when to start and stop wo
    interaction w provider
  - broad ntwk access: service is available over many ntwks and devices
  - resource pooling: provider makes rss pool and dynamically allocates per
    request
  - rapid elasticity: to consumer, rss pool appears unlimited; responds quickly
    and expands
  - measured service: provider can measure usage and report for billing 
* infrastructure as a service (iaas)
  - specify specs and rss wanted on a vm set
* software as a service (saas)
  - runs a prgrams
  - ex. google drive, dropbox
* dev platform as a service (paas)
  - come with ides 
  - continuous integration that allows devs to update code and auto test and
    deploy into a large software pkg
* wan to cloud
  - gives aglity and flexibility, migration is easy, and users can be distrib
  - cons: security is an issues, capacity w network traffic increases, qos is
    an issue, and isps typically dont provide sla for wan performance
    * can use private wan or vpn tunnel
    * xchg bw clouds also works
* virtual ntwk funx and services
  - netwking wi public cloud (dns, dhcp, etc)
  - virt ntwk funx (vnf): virt instance of ntwking device that can be run in
    a cloud
  - dns can be poited towards the cloud servers
  - dhcp: config thru vnf
  - ntp can be synced with enterprise's location as master

### 28. sdn and ntwk programmability
