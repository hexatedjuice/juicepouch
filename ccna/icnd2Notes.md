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

### 9. understanding eigrp concepts
### 10. implementing eigrp for ipv4
### 11. troubleshooting ipv4 routing protocols
### 12. implementing external bgp
## iii. wans
### 13. implementing p2p wans
### 14. private wans w ethernet and mpls

