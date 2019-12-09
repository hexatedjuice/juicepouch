# ccna
## I. intro to networking
### 1. intro to tcp/ip
* application, transport, network, datalink, physical
* datalink frames
	- a chunk of data over datalink
		* also inc mac address, ie datalink layer info
		* ex. ethernet frame
	- vs packet: chunk of data over ip
	- vs segment: chunk of data over trasnport
* osi vs tcp/ip
	- 7 layers in osi (+session,presentation)
	- encapsulation in osi: protocol delivery unit (pdu)
		* prefixed l\*pdu, where \* is the layer \#
### 2. fundamentals of ethernet lans
* access point vs switch
	- ap provide wireless access to wired network
	- switch needed to ctrl rest of the lan network
* ethernet: fam of standards (begin 802.3\*)

	speed | common name | informal ieee | formal ieee | cable
	--- | --- | --- | --- | ---
	10 mbps | ethernet | 10base-t | 802.3 | copper, 100m
	100 mbps | fast ethernet | 100base-t | 802.3u | copper, 100m
	1000 mbps | gigabit ethernet | 1000base-lx | 802.3z | fiber, 5000m
	1000 mbps | gigabit ethernet | 1000base-t | 802.3ab | copper, 100m
	10 gbps | 10 gig ethernet | 10gbase-t | 802.3an | copper, 100m

* utps (unshielded twisted pairs)
	-  ending data requires following an encoding scheme
	- twisting wires cancells out crosstalk emi
* small form-factor pluggable (sfp)
	- allows for additional ports to be customized
*  gigabit ethernet interface converter (gbic): og form factor; larger than sfps
* small form factor pluggable plus (sfp+)
	- same size sfp but faster speed (10gbps)
* straight through cable pinouts
	- 10base-t and 100base-t use 2 twisted pairs
	- nic transmitters use pins 1, 2 and transmit pins 3, 6
		* opposite for ethernet nics
	- pinout refers to the wiring of which color cables ares aligned
	- with direct ethernet communication, crossover cables necessary
		* ie. 1,2 cross over to 3,6
	- *know pc nic vs ethernet nic pinouts*

	transmit 1,2 | transmit 3,6
	--- | ---
	pc nic | hubs
	router | switches
	wireless ap (ethernet interface) | --

* utp cabling pinouts for 1000base-t
	- 4 wire pairs (1,2-3,6 and 4,5-7,8)
* fiber optic cabling
	- light reflects off of cladding through core
		* streams of data w different angles
			- multimode (mm)
		* single laser
			- single mode (sm)
	- necessary for two cables, tx and rx
* ethernet data-link structure

	field | bytes | desc
	--- | --- | ---
	preambel | 7 | syncing
	start frame delimiter (sfd) | 1 | signifies dest mac beginning
	dest mac | 6 | id recipient
	source mac | 6 | id sender
	type | 2 | defines protocol type (ipv4\ipv6)
	data and pad | 46-1500 | holds higher lvl data
	frame sequence check (fsc) | 4 | provide method for reciever to determine whether transmission errors

* ethernet addressing
	- typically macs are unicast
		* one device/nic per mac
	- manufacturers are assigned a 3 digit oui (org unique id)
	- group addressing
		* broadcast address: frames to the address are to be delivered to all on lan
			- ffff.ffff.ffff
		* multicast address: will be copied and forwarded to a subnet
* type field
	- "ethertype"
	- directly help network processing (ids type of networklayer/layer3 protocol within the ethernet fram)
		* ipv4:0800 ipv6:86dd
* error detection with fcs
	- similar to hash checking
* sending ethernet frames w switches and hubs
	- full duplex: simultaneous 2way comm
		* refered to as ethernet point-to-point
	- half duplex: 2way comm but not simultaneous
		* before switches, lan hubs
			- lan hubs are purely layer 1 devices, which forward using physical standards
			- simply repeat all msgs again
				* msgs can become garbled with overlap simultaneous
			- use csma/cd carrier sense multiple access with collision detection
				* takes care of obvious collisions and bad timing
				* can send jamming signal to tell collision occurred, independently choose random time to wait before retry
			- any ports connected to hubs must use half-duplex
			- referred to as ethernet shared media
### 3. fundamentals of wans and ip routing
* leased line wans
	- 2 directional, predetermined speed, fullduplex logic
	- telcos est a large network of cables and switches
		* service is offered to use this network
	- name refers to the fact that it is not owned but rented

	name | meaning/ref
	--- | ---
	circuit, link | same as line
	serial | bits flow serially and routers user serial interface
	point to point | topology is bw 2 pts only
	t1 | specific leased line transfer rate 1.544 mbps
	wan link | vv general
	private | data sent over line cannot be copied by other telco customers

	- layer 1
	- datalink layer protocols: high lvl data link ctrl (hdlc) and point to point protocol (ppp)
		* while hdlc has an dest address field, it is redundant as there is only one other connection
		* hdlc does not have "type" header so cisco uses proprietary w type
	- require de/re-encapsulation lan > wan > lan (802.3 > hdlc > 802.3)
* wan ethernet
	- layer 2 
	- "ethernet emulation": emphasize link is not a literal ethernet link end to end
	- EoMPLS: multiprotocol label switching, which sets up ethernet service
* ip routing
	- logical details
	- host fowarding logic: default gateway default when dest is not in same group
	- xrs networks: each router has ip routing tables to tell whereto fwd packet
	- routers reincapsulate datalink head/tail
		* arp (address resolution protocol): dynamically learns datalink addr of an IP host connected to a lan; used to link ip to mac address
* ip header
	- 32bit source and 32bit dest
	- 20byte total
	- remains unchanged in routing, only datalink replaced
* arp in depth
	- arp request: reply w mac if ip match
	- store info in arp cache/table
* ping ( packet internet groper)
	- uses icmp for echo request
	- response w echo reply
	- tests ip connectivity, layer 1-3
* each site has customer premise equipment (cpe) which includes router, serial intf card, and csu/dsu
	- serial intf card basically equiv of ethernet nic 
	- physical link req a funx called channel service unit/data service unit 
	- cabling includes short serial cable if outside csu/dsu is used
* csu/dsu provides funx called clocking which tells router exactly when to send each bit thru signal over serial cable 
	- router serial intf can prvide clocking but router cannot unless config with the `clock rate` cmd
### 4. fund of tcp/ip transport and app
* tcp/udp features

funx|desc
---|---
multiplexing using ports|allows rec hosts to choose correct application for which data is destined, based on port #
error recovery (reliability)|prcs of #ing and acknowledging data w seq and ack fields
flow ctrl w windowing|use window sizes to protect buffer size
connection est and term|inti port # and seq/ack fields
ordered data transfer and seg|cont stream and keep bytes in same order

* multiplexing: routes data to appropriate app
  - solve issue of multiple app packets by attaching port number with tcp/udp header
* the www consists of all interconnected web services and hosts
  - uri (uniform rss id): essentially clicking on a linking or entering
    equivalent in addr bar
    * url is a subset of uri
  - file transfer w http
    * http has multiple cmds eg. get
    * web pages usually have multiple objects
      6 server grabs first file to reference other uris to grab other objects
* ip header contains ip protocol fiel (like ethertype) specifies whih transp
  protocol (6 for tcp, 17 for udp)

## II. implementing ethernet lans
### 5. using the cli
* for intf with multiple compatible speeds, referred to as max speed, no matter what is in use
* cisco ios (internetwork os) 
	- ssh, console, telnet access
		* older consoles use utp cables to connect to serial port
	- emulators tend to have 8ni (8bps, no parity bits, 1 stop bit)
	- exec (user), enable/priv (cmds which may disrupt), config (chg config)
		* must go thru user > priv > config
	- interface to intaxn
	- line console 0 to go to line onfig instead of global config
	- config only modifies ram (running config file)
		* `copy running-config startup-config` (mv running settings to nonvolatile mem)
	- to clean existing config:
		``` 
		erase startup-config
		delete vlan.dat
		reload
		hostname $hostname
		```
### 6. analyzing ethernet lan
* switches actions
	- deciding when to forward a frame based on dest mac
	- preparing to forward frames by learning macs and examining source mac
	- prep to forward only 1 copy of frame by creating a layer 2 loop-free enviro w other switches using stp (spanning tree protocol)
* switches learn macs by adding frames w unknown source macs to table
* unknown dest mac results in flooding 
	- unknown dest mac called "unknown unicast"
	- stp: ensures that flooded frames do not loop indefinitely
* cisco switch defaults:
	- interfaces default enabled
	- all vlan 1 asmt
	- stp enabled
	- mac learning, flooding, logic etc
	- 10/100, 10/100/1000 negotiation
* to see learned mac addr `show mac address-table dynamic`
* commands various
	- `show interfaces f0/1 counters` shows stats on in/out frames on ports
	- filters exist eg. filter for ip addr in mac table
		*find macs learned off one a port add `interface $port`
			- can also specify vlan
* mac addr can age out on switches ~300s (aging-time)
	- if table fills, oldest are removed
* lan topologies
  - two tier campus design (collapsed core)
    * called collapsed bc there is no core layer
    * supports a distribution and an access layer of switches
      - access switches connect directly to users
      - distriution switches provide a path thru which access switches fwd to
        eo
    * provides a place for end users to connect (access layer) and connects the
      switches w a reasonable amt # of cables and switch ports w two
distribution switches as distrib
    * hybrid design wih a star layer as access and partial mesh at the
      distribution layer
      - no access layer switches interconnect
  - star: a design where central dev connects to several others 
  - full mesh: for any set of netwk nodes, a design that links bw each pai of
    nodes
  - partial mesh: for any set of netwk nodes, connects a link b some pairs of
    nodes but not all
  - hybrid: combines topology into more cmplx design
  - three tier campus designs (core)
    * can save wiring as 3tier, partial mesh works like 2tier full mesh
    * access: connection pt for end users 
    * distrib: aggreg for access switches and provids conn for rest of lan fwd
      bw switches
    * core: aggreg distrib switches in large lan, to inc fwd rate
* enterprise wlans and wlan ctrlers
  - issue: if you connect to many aps in a day, then all aps would have to know
    abt every othe wlan
  - solution: remove ctl and mgmt from ap and use wireless lan controller (wlc)
    * ap not referred to as lwap (lightweight ap) 
      - uses protocols like capwap (control and provisioning of wireless access
        points)
    * wlc keeps track of packets and end device locations (ie. which ap)

### 7. config basic switch mgmt
* vty (virtual teletype): cli allows remote connection via telnet/ssh
* can set diff pwd for vty and console logins
	- `line con(sole) 0` + `password $pwd` + `login` (enables usage of simple pwd to login)
	- `line vty 0 15` + `password $pwd` + `login`
		* specify lines 0 to 15

* local usr/pwd
	- globally set usr/pwd: `username $user secret $pwd`
	- specify console or vty and use `login local` to use local usr/pwd
	- (optional) clear out shared pwds with `no password`
* external server auth
	- AAA (accounting) server
	- usually using radius or tacas+ protcol
* ssh config
	- gen-key `crypto key generate rsa`
 	- v2 ssh `ip ssh version 2`
		* enable local login 
* control vty support: `transport input {all|none|telnet|ssh}`
* switched virtual interface (svi) 
	- also called vlan intf
	- uses vlan for ip config (most coo=mmonly vlan 1)
		* switch can send/rec frames on any ports in vlan
	- there are often multiple vlans
	- config the ip addr on one vlan intf allows switch to send/rec packets w other hosts that exist on _that_ vlan
		* cannot comm outside local subnet wo default gateway
			- configured pointing to a router's ip
* config ipv4 on a switch
	```
	configure terminal
	interface vlan 1
	ip address $addr $mask
	exit
	no shutdown
	ip default-gateway $gatewayaddr
	(optional) ip name-server $addr1 $addr2... " command in global config mode to configure switch to use dns
	```
	- to configure ip w dhcp use `dhcp` as param in `ip address $addr`
* verify ipv4 on switch
	- can use various:
		* `show runninf-config`
		* `show interfaces vlan $vlan`
		* `show dhcp lease` shows temp leased ip addr
	- know whether switch is dhcp config
		* if dhcp fails `show interfaces vlan $vlan` will not list ip addr
* misc cmds
	- `show history` shows list of cmd held in history buff
	- `terminal history size $size` set histoy buff size for current session
	- `history size $size` set history buff perm
	- `[no] logging console` to temp en/dis msgs that ios sends admin
		* `logging synchronous` show msgs at more convenient times, after show cmds
	- `exec-timeout $min $sec` special option 0 to nvr timeout
	- `no ip domain-lookup` there can be pause after mistype cmd due to ios interpreting it as an addr and using dns resolution, this disables that
* port security
  - config the switch as access or trunk
  -  activate with `switchport port-security`
    * you can override max allowed macs per intf w `switchport port-security
      maximum $max`
    * you can predefine allowed source macs w `mac-address $mac`
      - or stuff can be learned dynamically `mac-address sticky`
  - default max source=1 and default action=disable intf
  - sticky learned are not considered dynamically learned in mac table but as
    static
### 8. config and verify switch intf
* config speed, duplex, desc
	- multi speed intf will autoneg speed, but you can man config and duplex
		* `duplex {auto|full|half}` and `speed {auto|10|100|1000}`
	- `description $desc` allows to attach a desc like "end users attach here"
* can config a range of intf w `interface range $range` ex. "FastEthernet 0/11 - 20"
	- functionally, ios interprets this as if you had typed out config cmds for all intf in the range
* intf status cmds
	- `[no] shutdown` en/dis intf
	- `show interfaces $intf status` shows more succict info than `show interfaces $intf`
* disable configs with `no` ex. `no speed` or `no description`
* ieee autoneg (802.3u up)
	- both nodes with auto neg: will auto choose the best standards
	- one node funx: may cause connection issues
		* note: config speed and duplex on cisco switch disables autoneg
		* if autoneg fails ie. one node only/ no response:
			- default slowest speed 10mbps
			- if speed 10/100 use half, otherwize use full duplex
		* duplex mismatch can occur ex. a host w disabled autoneg has 100/full but switch assumes 100/half
			- host assuming full will not use csma/cd but switch with half will, thus the link will perform poorl as the switch will think that collisions are occuring and resend frames
* autoneg and lan hubs
	- hubs to not autoneg msgs nor fwd msgs
		* thus lan hub connected devices must use ieee defaults
		* devices onnected to lan hubs must also use half duplx bc hubs use csma/cd to avoid collisions
* debugging for nonworking states
	- `show interfaces` shows layer 1 stats
	- `show interfaces descriptions` shows layer 2 stats

	line stat| protocol stat|intf stat|typical root cause
	---|---|---|---
	administratively down|down|disabled|`shudown` is config on intf
	down|down|notconnect|no cable;bad cable; wrong pinouts; speed mismatch; neighboring device is off
	up|down|notconnect|not expected on lan switch phys intf
	down|down(err-disabled)|err-disabled|port sec has been disabled on intf
	up|up|connected|intf is working

* duplex config
	- any config prefixed w `a-` is auto config
	- even if autoneg fails, config default marked as `a-` and will still be up/up
		* must check both ends to make sure no problem
* common layer 1 problems
	- any up/up state considers intf to be working 
	- if any bits have been altered it is notified by fcs
		* marked as a crc error (cyclic redundancy check)
	- runts: frames not at min req size (64bytes), can be caused by collisions
	- giants: exceed max size (1518 bytes)
	- input error: total counter of runts, giants, no buffer, crc, frame, overrun, and ignored counts
	- crc: frames that did not pass fcs check
	- frames: recieved frames w illegal format ex. partial byte, can be caused by collsion
	- packet output: packets fwd from intf
	- output errors: total of attemped th=ransmissions that failed
	- collisions: counter of all collisions in transmission
	- late collisions: subset of collisions that happen after 64th byte in frame, often points to duplex mismatch bc it should occur w/i first 64 bytes
		* this is bc the full duplex intf just keeps sending frames even as half intf pauses
	- up/up state can still indicate bad cabling, note increases in crc count
## III. implementing vlans and stp
### 9. implementing ethernet virtual lans
* one def on a lan can be all dev on same broadcast domain, when a broadcast frame is sent all dev get it
	- by default, switches consider all intf as part of one broadcasting domain
* instead of 2 phys switches to create 2 broadcast domains, you can use 2 vlans
* vlans can reduce overhead and increase security
	- you can specify secpol for each vlan
	- can group users by dept etc instead of by location
	- reduce workload for stp by limiting vlan to single acess switch
* multiswitch vlans w trunking
	- single switch vlans only need to be told which ports are which vlan #
	- vlan trunking uses vlan tagging: the sending switch attaches another header to the frame before sending to trunk, which includes a vlan id
	- you can create multiswitch vlans without trunking by using links
		* does not scale well
	- vlan tagging concepts
		* trunking creates one link bw switches that sypoorts as many vlans as needed
		*  switches treat link as if part of all the vlan
			- trunk keeps vlan frames separate bc each frame is id by vlan # as cross link
		* allows switches to fwd frames from mult vlans over single phys connection by adding small header to the ethernet frame
		* as the switch recieves the frame, it removes vlan header and fwds og frame to the specified vlan
	- 802.1q and isl (interswitch link) trunking
		* 802.1q is more pop and newer
			- adds 4byte vlan header as "tag" in packet
				* inc the 12bit vlan id
			- supports 4094 vlans (0 and 4095 are reserved)
		* two ranges 1-1005 and extended 1006-4094
		* 802.1q defines one vlan id on each trunk as the "native vlan"
			- no header required for this and is understood as native/default
			- helps to support dev who do not understand trunking
* routing bw vlans
	- layer 2 switches perfor logic per vlan
		* the switch acts as diff switch per vlan
	- to fwd bw vlan the network must use a router device
		* some swithes have this funx as a layer 3 switch
		* with separated router, the router fwds the packet into diff port of switch in the desired vlan
* vlan and trunking config and verif
	- creating and assigning access clans to an intf
		* `vlan $vlanid`
		* config name w `name $name` in conig mode
			- default is "vlanzzzz" where zzzz is the vlan id
		* interface each intf in that vlan and use `switchport access vlan $vlanid` to assign vlan id to that intf
		* (optional) use `switchport mode access` cmd to make this port always use access mode (does not use trunking)
		* `show vlan brief` shows quick vlan overview
		* `show vlan id $id` shows overview of specific vlan
		* switch can dynamically create a vlan if `swithport access vlan $vlanid` refers to an unconfigured/undefined vlan
	- vtp (vlan trunking protocol) cisco proprietary
		*advertises each vlan in one switch so other switches an learn
		* usually disabled: `vtp mode off` or `vtp mode transparent`
		* switches w vtp can only use vlan 1-1005 and client switches cannot configure vlans
			- servers and clients can learn new vlans and have their own vlans deleted bc of vtp
	- vlan trunking config
		* static config 
		* `switchport mode trunk`
		* can be set to negotiate settings in administrative mode
			- using dtp (dynamic trunking protocol) can negotiate whether to use isl or 802.1q
				* `switchport trunk encapsulation {dot1q|isl|negotiate}
				* 'switchport mode {access|trunk|dynamic desirable|dynamic auto} desirable sends neg msgs and responds to dynamically choose whether to use trunking, auto passively waits for neg msgs and respond

admin mode|access|dynamic auto|trunk|dynamic desirable
---|---|---|---|---
access|access|access|do not use|access
dynamic auto|access|access|trunk|trunk
trunk|do not use|trunk|trunk|trunk
dynamic desirable|access|trunk|trunk|trunk

	- usually trunk neg disabled on most ports for sec
* data and voice lan
	- before ip telephony, phones ran on separate routes than pcs using a voice switch or private branch exchange (pbx)
	- in order to resolve the porblem of running two cables, ip phones have embedded switches
	- data (pc) and voice vlans
		* voice vlans are usually tagged with 802.1q header
	- config and verif
		* initiate config with `switchport mode access`
		* specify voice with `switchport voice vlan $vlanid`
		* specify data with `switchport access vlan $vlanid`
	- configure like normal access port and define voice vlan
		* check status with `show interfaces $type $number switchport` 
* debug vlan and vlan trunk
	- check all vlans defined and active
	- check allowed vlan lists on both ends of trunnk to ensure all vlans inted to be used are included
	- check incorrect trunk config where only one switch is config as trunking
	- check that native lan settings match
* undefined/disabld access vlans
	- switches do not fwd frames to vlans that are:
		* no known bc vlan not config/not learned w vtp
		* vlan is known but disabled
	- enable `no shutdown` on vlan
	- vlans are either active or act/lshut
		* act/unsup means it is an unsupported vlan for vlan id 1002-1005
* mismatched trunking operational states
	- common mistake where both switches using mode dynamic auto
	- it can also be that one switch trunks but the other switch does not
		* thus the one that does not will discard frames with a 802.1q header
		* only native headers will pass
* supported vlan list for trunking
	- vlan has not been removed from allowed vlan list on trunk `switchport trunk allowed vlan`
	- vlan exists and is active on local switch `show vlan`
	- vlan has not been vtp-pruned `show spanning-tree vlan $vlanid`
	- `show interfaces trunk` also shows shows allowed vlan ids
		* default 1-4094 allowed

	heading|reason
	---|---
	vlans allowed|vlan 1-4094, minus those removed by `switchport trunk allowed {param}`
	vlans allowed and active|first list minus vlans not defined to that local switch (that is, there is not a vlan global config command or the switch has not yet learned of the vlan w vtp)
	vlans in spanning tree|second list minus vlans in an stp blocking state for that intf and mine vlans vtp pruned from that trunk

* mismatched native vlan on trunk
	- it will cause sent frame to jump vlan to vlan
	- this is called vlan hopping
### 10. spanning tree protocol
* stp and rstp (rapid stp)
	- wo it, frames could loop indefinitely
	- stp and rstp intelligently block ports
	- performs check: if port is in stp/rstp fwding state in that vlan proceed as normal, if it is blocking, block all user traffic and do not sned/rec user traffic on that intf in vlan
		* its status is an addiitonaly one, over that of eg. up/up
* stp overview
	- prevents 3 common problems in ethernet lans: indefinitely looping frames
		* looping frames called broadcast storm 
### 11. troubleshooting ethernet lans
* troubleshooting steps
  - isolate pblm and document
  - resolve or escalate
  - verify or onitor
* analyze fwding path
  - summary of fwding logic including lan switching:
    1. prcs funx on incoming intf, if intf is up/ip then:
      - if configed, apply port security to filter as apporpriate
      - if it is access, determine intf's acces vlan  
      - if it is trunk, determine the frame's tagged vlan
    2. make fwding decision. look for dest mac but wi the tagged vlan. if dest
       mac is...
      - found (unicast): fwd frame only out the intf matched in the entry
      - not found (unicast): flood frame (except inc port) in matching tagged
        vlan an dtrunks that have not restricted that vlan 
      - broadcast: flood the frame following prev step's rules
* analyzing port sec on intf
  1. id all intf which port sec is enabled (`show running-config` or `show port
     security`)
  2. determine whether sec violation is currently occuring based on violation
     mode of port sec config
    * shutdown: intf will be `err-disabled` and port sec status will br
      `secure-down`
    * restrict: intf is connected but port sec stats will be `secure-up`, `show
      port-security interface`will show incrementing violations counter
    * protect: intf will be connected and `show port-security interface` does
      __not__ show inc violations counter
  3. in all cases, compare port sec to diagram and to the last src addr fild in
     the output of the `show port-security interface` cmd
  - to recover from the secure-shutdown state the intf must be `shutdown` then
    reenabled w `no shutdown`
  - difficult to analyze info with "protect" mode on
    * no logs, only has last mac address intaxn w 
  - with restrict there are syslog msgs and violation counter
* analyzing vlans and trunks
  1. id all access intf and assigned access vlans; reassign as needed
  2. determine whether vlan exists and are active on each switch
  3. check allowed vlan list on both switches on trunk, make sure they match
  4. chek for incorrect config settings that result in trunk mismatc (ie. one
     acts like a tunk, the other doesnt)
  - make sure you configure no shutdown on vlans to enable them
  - situation ex: sw1 is static trunking and with dtp off, sw2 has dtp dynamic
    desirable. thus no trunking occurs as sw2 recieves no response to dtp
requests
## IV. ipv4 addr and subnetting
### 12. perspective on ipv4 subnetting
* an ip subnet is a subclass of an A-C netwk
* addr in same subnet are not separated by routers
* addr in diff subnet are separated at least by one router
* plan for a subnet per vlan, ptp serial link, ethernet emulation wan link
  (eompls)
* choosing classful netwks
  - implementation of nat (network addr transl) for new private netwrks
    * defined by rfc 1918

class|priv ip|# of netwks
---|---|---
a|10.0.0.0|1
b|172.16.0.0-172.31.0.0|16
c|192.168.0.0-192.168.255.0|256

* host bits are borrowed to create subnet bits
* static and dynamic ranges per subnet
  - hosts can recieve ips from dhcp
    * can configure range on dhcp (ie. reserve lower or higher ranges for
      static ocnfig addr) 
### 13. analyzing classful ipv4 netwks
* be able to determine from an ip addr:
  - class (a,b,c)
  - default mask
  - number of netwk bits/octets
  - number host bits
  - number of possible host addr 
  - netwk id
  - netwk broadcast addr
  - first and last usable addr in netwk

class|first octet|purpose
---|---|---
a|1-126|unicast (large netwk)
b|128-191|unicast (med netwk)
c|192-223|unicast (small netwk)
d|224-239|multicast
e|240-255|reserved

* steps to determine
  - determine class based on first octet
  - to find network number change host bits to 0
  - to find first addr, add 1 to the last host bit
  - to find broadcast addr change host octets to 255
  - to find last broadcast addr, subtract 1 from the fourth octet of the
    broadcast addr
* unusual netwk id and broadcast addr
  - class a
    * loopback addr 127.0.0.1
    * 0.0.0.0 reserved for broadcast req
  - make sure to know cutoffs for a,b,c, can be easy to mistake
### 14. analyzing subnet masks
* subnet mask conversion
  - ddn 
  - binary
  - prefix notation
    * prefix masks are based upon'
    * aka cidr (classless interdomain routing) masks
    * basically indicate how many bits are taken by the mask
      - eg. 11111111 11111111 11111111 11110000 > /28

binary octet|dec
---|---
00000000|0
10000000|128
11000000|192
11100000|224
11110000|240
11111000|248
11111100|252
11111110|254
11111111|255

* id subnet design choices w masks
  - maks refered to as prefix bits, w others as host bits
  1. convert maks to prefix fmt as needed
  2. determine netwk mask based on class
  3. subet mask = prefix - network
  4. host = 32- prefix
  5. hosts/subnet = 2^hosts - 2
  6. caalculate number of subnets 2^subnet mask
### 15. analyzing existing subnets
* lowest and highest addr reserved for id and broadcast respectively
* find subnet addr given number of subnets
## V. implementing ipv4
### 16. operating cisco routers
* branch and main office can be connected iwth a serial link
  - csu/dsu unit u=installed on ither end to interpret signals
  - use rj48 connectors (same size as rj45)
* cisco integrated service routers
  - they do more than routing packets (ie switching etc)
  - netwk intf modules (nims)
* physical installation
  1.  connect lan cables to lan ports
  2. if using external csu/dsu connect router serial intf to csu/dsu an dthe
     csu/dsu line to telco line
  3. if using an internal csu/dsu connect router serial intf to telco line
  4. connect router console port to pc (rollover cable) to config router
  5. connect power cable from pwr oulet to power port
  6. power on router
* can also use dsl w catv cabling
* bandwidth and clock rate on serial interfaces
  - default is 2000000 for clock rate
  - clock rate ctrls layer 1 speed on the link
  - bandwidth does not impact speed but is used for documentation and an dinput
    for other prcs
    * ex. ospf and eigrp (enhanced interior gateway routing protocol) base
      their routing metrics off of bandwidth
* router aux port
  - serve as a means to make phone call to connect into router to isse cmds
    from cli
  - funx as sort of console port but must be connect through an external
    analogue modem and then the telephone line
  - can be config with `line aux 0`
 
serial line status|protocol status|typical reasons
---|---|---
admin down|down| shutdown config
down|down|physical issue
up|down| data link problems, usually config 9ex. one uses ppp one hdlc)
up|up|layer 1 and 2 ok

### 17. config ipv4 addr and static routes
* config ip addr and connected routes
  - cisco default global ipv4 routing
  - can add routes thru 3 methods:
    * connected routes: added from config ip addr intf on router
    * static: added bc of config `ip route` cmd on local router
    * routing protocols: added as funx by config on all routers resulting where
      each router dynamically tells eo routes to learn
  - connected routes added throug `ip address` cmd 
    * `show ip route` should list as "c" for the route code meaning connected
* arp table on cisco router
  - lists ipv4 and matching mac of hosts connected to same subnet as router
* routing bw subnets on vlans
  - options:
    * use router w one router lan intf and cable connected to the switch for
      each and every vlan (typically not sued)
    * use router w vlan trunk connecting to lan switch
    * use layer 3 switch
  - configuring routing to vlans using 802.1q on routers
    * referred to as roas (router on a stick)
    * roas uses router vlan trunking config to give router a logical intf
      connected to each vlan
    * since only one real intf used on router, virtual subintf created
      - example: a divided G0/0 intf can be divided into G0/0.10 an G0/0.20 for
        vlan 10 and 20
  1. use `interface type number.subintf` in global to create unique subintf for
     every vlan
  2. use `encapsulation dot1q vlan_id` in subintf cmd to enable 802.1q
  3. use ip addr cmd to set ip settings (addr and mask)
  - the encapsulation cmd is what definess the subintf instead of the intf name 
    * config ip on phys intf but wo encapsulation cmd
    * ip addr cmd to config subintf and use encapsulation ... native subcmd
  - consig routing to vlan w layer 3 switch
    * same config as a layer 2 switch 
      - needs virtual intf connect to each vlan internal to the switch
      - has a routing table
    1. for those that support ipv4 routing use `sdm prefer lanbase-routing` and
       `reload`
    2. use ip routing cmd in global config to enable ipv4 routing
    3. use `interface vlan` to create vlan intf for each vlan
    4. use `ip address address mask` to config ip addr and mask on vlan intf
    5. use `no shutown`
* configure static routing
  - static routes can be defined with `ip route`
    * next hop can be defined wither via interfac or ip addr
      ```
      ip route 172.16.2.0 255.255.255.0 172.16.4.2
      ip route 172.16.2.0 255.255.255.0 S0/0/1
      ```
  - there can also be static routing for indiv hosts
  - static routes with no competing routes
    * even if there are no competing routes, it must consdier:
      - is the interface in up/up
      - local router must have a route to that addr
  - static routing w competing routes
    * there are multiple routes to one addr
    * static is preferred over ospf/other protocol learned
      - to prevent this, use floating static route
        * you can override the admininistrative distance
        * add a distance variable when configuring ip route
* static default routes
  - default to forwarding packets down a specific interface
  - `ip route 0.0.0.0 0.0.0.0 s0/0/1`
  - gateway of last resort
  - displayed as static (s) but with an asterisk which shows its a candidate
    default route
* troubleshooting static routes
  - incorrect static routes that appear in ip routing table
    * is there an incorrect mask
    * is next hop correct
    * is outgoing intf correct
  - static route does not appear in the ip routing table
    * ip outes can be accepted when typed in cli but does not appear in table
      (when type `show ip route`) 
      - outgoing intd listed in ip route is not up/up
      - next hop router is not reachable
      - a better competeing route exists (lower admin distance)
### 18. learning ipv4 routes w ripv2
* rip and routing protocl concepts
  - history of interior gateway protocols
    * wave 1(distance vector): ripv1 igrp, 2(ipv4):ospfv2 eigrp ripv2,
      3(ipv6):eigrpv6 ospfv6 ripng, 4(ipv4+ipv6): ospfv3 addr-families
  - comparing igps 
    * ospfv2 and eigrp used most (ripv2 much less)
    * gateay == router
    * points of comparison
      1. underlying algorithm: whether it uses distanc evector (dv) or link
         state (ls)
      2. usefulness of metric: how good it choosing best path
      3. speed of convergence: how long it takes for all routrs to learn
         a change in netwk
      4. public standard vs vendor-proprietary: rip and ospf are standards,
         eigrp is cisco, kept private until 2013
    * rip uses "hop count" and each router is a hop to measure distance
    * newer routing is link based and takes speed into acocunt
  - dv basics
    * full update msgs and split horizon
      - ripv2 uses periodic updates
        * ex. r2 has subnet in up/up state and addr so it adds it to its own
          routing table and sends the route to r1 w metric 1 (hop 1) which it
then adds to its table
    * split horizon refers to how some routes are ommitted in the update msg,
      so it wont send the other router info it already knows
    * route poisoning
      - dv prevents loops by informing every router of failed route asap
      - means advertising failed route (advertised with infinity metric as
        special case, defined by rip as "16")
  - ripv2 stuff that ripv1 lacks
    * authetication
    * manual route summ (decrease size of routing table)
    * uses 224.0.0.9 multicast ip while ripv1 used 255.255.255.255
    * supports vlsm (variable length subnet masks)
* core ripv2 config and verif
  - core rip features:
    * `router rip` into config
    * `version 2` to switch to v2
    * use 1+ `network $number` cmds in rip config to enable rip on correct intf
      - one netwrk num can cover multiple intf if under same netwk range
  - once enabled:
    * router sends outing updates out the intf
    * router listens for and prcsses incoming updates on intf
    * router adv abt subnet connect ed to intf
  - verif
    * `show ip route rip` routes: lists ipv4 routes learned by rip
    * `show ip protocols` config: lists info abt rip config plus ip addr of
      neighbor rip routers from which the router has learned routes
    * `show ip rip database` best routes: shows prefix/length of all bets
      routes known to rip on this router
  - comparing routes w admin distance
    
    route src|admin d
    ---|---
    connected|0
    static|1
    eigrp|90
    ospf|110
    rip|120
    dhcp default|254
    unknown/unbelievable|255

* optional rip2 config and verif
  - ctrl rip updates w `passive interface`
    * need to adv subnet but not routes
  - supporting multiple equal-cost routes w maximum paths
    * when metrics tie, rip splits packets and sends some over both
    * "equl cost load balancing"
  - auto summ and discontiguous classful netwks
    * older protocols (ripv1 igrp) classful routing 
      - needed to avoid discontiguous netwks bc they auto-summ
    * autosumm when: one router connects to multiple diff classful netwks, when
      router uses protocol w autosumm feature
      - ex. router connected to 10.3.. 10.4.. and router connected 10.1..
        10.2.. would auto summ and advertise as
        10... but then the neighbor only learns 10... from both no subnets and
confused
      - contiguous: subnets of netwk x are not separated by subnets of any
        other classful netwk
    * disable auto summ to let it adv subnets `no auto-summary`
  - verif optional rip features
    * `show ip protocols`
    * evidence of load balancing shown w `show ip route rip` two routes will be
      listed under one netwk
      - `maximum-paths  #` will limit the number of routes to each netwk
  - default routes
    * ripv2 can advertise default route
    * set gateway router `ip route 0.0.0.0 0.0.0.0 ....`
      - and use `default-information originate` to start adv 
    * via dhcp
      - gateway router can recieve dhcp info from isp router
      - `ip address dhcp`
      - only diff from static route in menu is admin d 254
* troubleshooting ripv2
  - symptoms w miss/incorr netwk cmds
    * r does not adc, r does not xchg routing info w other rs
  - passive intf pblms
    * do not use passive intf to another rip r
      - in which case on r would keep sending updates while the other would not
  - autosumm issues
    * sometimes no effect, but when 3+ classful to r, subnets may not be
      completely/corr adv
  - rip issues via othr router features
    * intf must be working for rip to funx
    * two r on same link must have ip addr in same subnet for ripv2 to xchg
      routing info
    * als can filter rip msgs and accidentally break rip 
### 19. dhcp and ip netwk on hosts
* implm and troubleshooting dhcp
  - used to auto assign ip and masks to host dev
  - to lease an ip
    * discover: sent by dhcp client to find dhcp server
    * offer: sent by dhcp server to offer lease to client w specific ip
    * request: client asks for the ipv4 in offer
    * ack: server assigns addr, adds to list th maks, def r, and dns server ip
      addr
  - bc discover dev does not have ip yet, use special
    * .... addr reserved as src fot hosts wo ip
    * 255.255.255.255 local broadcast ip, packets to this dest are broadcast on
      local data lik but routers do not fwd
  - support dhcp for remote subnets w dhcp relay
    * dhcp servers can be located in every subnet or in a central site
    * to make conn w remote netwk
      - ` ip helper-address`
        * it is an intf subcomand that watches incoming dhcp msgs w dest ip
          255.255.255.255
        * changes ip src to router incoming intf ip addr
        * chg packets dest ip adr to that of the dhcp server (as configured in
          ip helper)
        * route packet to dhcp server
  - info stored at dhcp server
    * subnet id and mask: used to know all addr wi subnet
    * resevred addr: allows engineers to reserve static use addrs
    * def r: ip addr of r on a subnet
    * dns ip addr: list of dns server ips
  - allocation modes
    * dynamic alloc, auto alloc (lease time inf), static alloc (preconfig
      specific ip for hosts based on mac addr)
  - dhcp server config on routers
    * config r w dhcp (one per subnet) is called dhcp pooling
    * cisco ios dhcp config:

```
ip dhcp excluded-address $first $last   # to reserve addr
ip dhcp pool $name                      # to create dhcp pool for subnet 
network $subnetid $prefix               # define subnet
default-router $addr1 $addr2...         # define default router ip addr
dns-server $ip                          # specify dns server
lease $days $hrs $min                   # define lease time
domain-name $name                       # config dns domain name
next-server $addr                       # define tftp server 
```

  - ios dhcp server verif
    * `show dhcp binding` show current leased addr
    * `... pool $poolname` list config range of addr + stats for surrently
      leased addr
    * `... server statistics`
  - troubleshooting
    * relay agent config mistakes
      - misconfig ip-helper
      - relay is only neeed if dhcp server is on another subnet
      - trunk subintf (roas) also need iphelper
    * server config mistakes
      - packet from relay agent to dhcp uses intf addr
      - dhcp server compares src ip to netwk cmds in dhcp pools to find right
        pool
      - if src ip addr of packet is not in range of addr implied, dhcp has no
        pool to use for response, thus no response
      - dns server ip misconfig > hosts fail to resolve hostnames into
        associated ip
      - default gateway misconfig hosts cannot config w ext netwk
      - tftp server misconfig, ip phone fails 
    * ip connectivity from dhcp relay agent to dhcp server  
      - ip vroadcast packets must flow bw client > relay > server
    * summ dhcp troubleshoot
      - centralized dhcp must have dhcp relay r on each remote subnet
      - centralized dhcp should have properly config pools 
      - troubleshoot for ip conn issue bw server and r using relay ip addr as
        src and server ip as dest
      - check conn bw relay and client
    * conflict w offered addr and used addr
      - server pings addr to see if used before assigning ip
      - `show ip dhcp conflict`
      - need to use `clear ip dhcp conflict` to allow dhcp server to offer
        these addrs again
- verifying host ipv4 settings
  * default routers
    - host and router link must be in same vlan
    - host and default r in same subnet
    - lan switch must not discrad packet bc of security or acl
- ipv4 addr types
  * ip broadcast 
    - local (255...)
    - subnet (can be calculated)
  * multicast
    - cn be sent to subnets only if listening for that addr
    - routers flood as if it were broadcast but only to those who registered to
      listen

type|ip type
---|---
common app|uni
assigned w dhcp|uni
use a,b,c|uni
overhead protocol (arp, dhcp)|broadcast
used as dest ip only|broad,multi
apps that send same data to multi clients|multi
class d|multi

## VI. ipv4 design and troubleshooting
### 20. subnet desgin
* choosing the best mask
  - maximize number of hosts per subnets: smallest prefix mask 
  - maximize subnets: use longets prefix mask possible
  - inc both subnets and hosts: choose mask in mid range
* finding all subnet ids
  - the lowest subnet id = network id
    * can be disabled for disambiguity w `no ip subnet-zero`
### 21. variable length subnet masks (vlsm)
* classles and classful routing protocols 
  - classless adv mask w each adv route

protocol|classless?|sends mask in updates|support vlsm|support manual route sum
---|---|---|---|---
ripv1|no|no|no|no
ripv2|yes|yes|yes|yes
eigrp|yes|yes|yes|yes
ospf|yes|yes|yes|yes

* config and verif
  - simply intf config each mask and addr
  - `show ip route` can chek for diff masks
* vlsm overlaps
  - cn result in duplicate host addrs
  - how to design w vlsm
  - make sure there is no stacking masks
* adding new subnet to existing vlsm
  - pick subnet mask based on req
  - find all possible subnet numbers 
  - make list of og broadcast and ids
  - rule out overlapping subnets
  - choose new subnet id from remaining
### 22. ipv4 toubleshooting tools
* problem isolation w `ping`
  - succ ping indicates uo/up, port sec not filtered, stp places right ports in
    fwd state
  - extended ping
    * can specify "src" addr to test connectivity
* test lan neighbos
  - if ping works can indicate onfig right and that r has learned macs
* using ping w names and ip addr
  - ping via hostname tests dns funx
* problem iso w `traceroute` cmd
  - id all hops bw host and dest
  - how?
    * increments ttl value to "traceroute" of packet 
  - can use extended as well
* telnet and ssh
  - may be useful to use ios builtin client
    * routes the instace of tty to desired addr instead of direct connection
### 23. ipv4 routing troublshooting
* issues bw host and default r
  - ensure ipv4 settings match
    1. check hosts list of dns server addr against actual addr
    2. check host default r against r's lan intf 
    3. check subn mask used by r an dhost match
    4. host and r are connect wi same subnet (same subn id and same ip range)
  - mismatched masks impact route to reach subn
    * ex. a host can send packets out but does not rec. r is misconfig mask
      which puts host outside of range
  - dhcp issues
    1. if using centralized server, each r must have `ip help-address` config
       as relay
    2. torubleshoot for connectivity bw dhcp relay and server w intfs as src
       and dest
    3. troubleshoot for local lan errors
    4. troubleshoot incorrect server config
  - r lan intf and lan issues

reason|desc|state
---|---|---
speed mismatch|both r and switch use `speed` but mismatch|down/down
shutdown at router|r config w `shutdown`|admin down/down
shutdown at switch|switch config `shutdown` but r is on|down/down
err-disabled switch|neighbor switch uses port sec|down/down
no cable/bad cable|no cable installed, pinouts incorr|down/down

* issues w routing bw rs
  - ip fwd by matching most spec route
    * overlap subnet cuase:
      - autosumm
      - manual route summ
      - static routes
      - incorr desg subnetting desg
  - recog whether or not using vlsm
    * os detects overlap on same r
## VII. ipv4 services: acl and nat
### 24. basic ipv4 acl
* r can appl al logic to packets at any intf 
* matching packets: how each packet analyzed by r
* types
  - standard 1-99
  - extended 100-199
  - additional (1300-1999, ext 2000-2699)
* standard numbered
  - matchs only src addr
  - list logic
    * first match logic
  - syntax: `access-list {1-99 | 1300-1999} {permit|deny} matching params`
  - matching w wildcards
    * 0: compare
    * 255: ignore octet
    * binary wildcards
      - subtract subn mask from 255.255.255.255 to find wildcard mask
* implementation
  1. plan location
  2. config acl w global config
  3. enable acl w `ip access-group $acl# {in|out}`
* troubleshootin and verif
  - can append `log` to end of acl to log traffic
### 25. adv 1pv4 acl
* extended numbered acl
  - match protocol, src, dest ip
    * "ip" to deny all packets
  - match tcp/udp port numbers
    * can be specified via `eq` 
    * besides port numbers also takes keywords like "telnet" and "www"
* named acl and acl editing
  - differences:
    1. names vs numbers
    2. use acl subcmds to define 
    3. use acl editing features that allow cli user to del indiv lines from acl
       and add new lines
  - edit acl based on seq num
* acl implementation considerations
  - place close to packet src > prevent packets from being missed
  - place near dest > make sure no packet unintentionally filtered
  - specificity
  - disable the acl `no ip access-group` before editing
* troubleshooting
  - analyzing behavior
    1. dtermine which itf enabled w acl `show running-config` or `show ip
       interfaces`
    2. find config of each acl `show access-lists` `show ip acces-lists` `show
       running-config`
    3. analyze acls to predict filtering
      - misordered statements
      - reversed src and dst
      - syntax
        * ex. needs `tcp` or `udp` in order to filter for port numbers
      - explicity deny any 
        * explicitly deny any at end of all lists
  - acl intaxn w r-generated packets
    * local acl and ping from r
      - r ignore acl w self-generated packets
    * self ping
      - just permit icmp
### 26. nat
* cidr (classless interdomain routing)
  - defines how to assign ip addr to allow route aggregation/summ 
  - isps can match w one route and then interpreted
  - ex. 200.1.3.0 is a class 3 /24, however can be shortened to /16 if owned
    all of 200.1..
* nat concepts
  - chg ip addr of host to that of src lan to communicate w outside world
  - static nat
    * ip addr are statically mapped to eo
    * one to one premapped
  - dynamic nat
    * a pool of public addr are given for use
* overloading nat w port addr translation
  - inc hosts req inc amt of registered ip addr
  - pat solves this (port addr translation)
    * use multi port instead of multi addr effectively reducing addr usage
* nat config
  - static nat
    1. `ip nat inside` on inside gate
    2. `ip nat outside`
    3. ` ip nat inside source static $insidelocal $outsideglobal` to make static
       mappings
  - dynamic nat
    1. `ip nat inside` `ip nat outside
    2. config an acl that matches packets enetering intf for which nat is
       performed
    3. `ip nat pool $name $firstaddr $lastaddr netmask $mask`
    4. `ip nat inside source list $aclnum pool $poolname` using created acl and
       pool
    * verif
      - `show ip nat statistics` and `show ip nat translations`
  - pat
    1. enable nat
    2. config acl
    3. `ip nat inside source list $aclnum interface $intf overload` to the intf
       whoose ip is used for translations
* troubleshooting 
  - traffic is required, no translations until traffic hits
## VIII. ipv6
### 27. fundamentals of ipv6
* intro to ipv6 
  - created to statisfy ip addr needs
  - header is 40 bytes
  - ipv6 routing protocols
    * ripng
    * ospfv3
    * eigrpv6
    * mp bgp-4 (border gateway protocol)
* formatting and conventions
  - full ipv6 addr
  - abbreviation
    * wi each quartet, remove leasing 0s except for last (eg. 0000 > 0)
    * any string of 2+ consecutive quartets of 0ncan be replaced to "::"
    * ex.FE00:0000:0000:0001:0000:0000:0000:0056 > FE00:0:0:1:0:0:0:5 > FE00:0:0:1::56
      - replace the longest seq of 0 quartets bc :: can only be used once
  - prefix lengths
### 28. ip addr and subnetting
* global unicast addr concepts
  - public and private ipv6 addr
    * global unicast: addr work like public ipv4 and must be registered
    * unique local: works like private ipv4 
  - ipv6 global routing prefix
    * network pits > global routing prefix
      - ex. iana > arin (2001:) > na-isp1 (2001:0db8) > etc. etc.

addr type| first hex prefix
---|---
global unicast|2 or 3 (og); all not reserved (today)
unique local|fd
multicast|ff
link local| f280

* subnetting w global unicast
  - host bits called interface id
  - basically same as ip4 lol
* unique local unicast addr
  - prefix fd + 40bit global id
  - the need for global unique local addr
    * can be created by choice (easy to remember and type)
    * however should follow rfc and use random gen
      - this makes mergers much simpler as in ipv4 many companies did servers
        under 10..., making it a headache to transfer
### 29. implementing ipv6 addr on rs
* implementing unicast ipv6 addr on rs
  - to transition to ipv6, dual stack implementation
    * r support ipv6 and hosts can switch whenever
* static unicast addr config
  - full 128b addr cconfig
    * `ipv6 address $addr/$prefix`
    * enable v6 routing `ipv6 unicast-routing`
    * verif w `show ipv6`
  - gen unique intd id with modified eui-64 (extd. unique id)
    * hosts can use dhcp or slaac (stateless addr autoconfig) to determine ip
    * eui64
      1. split mac into 2 6by chunks
      2. insert "fffe" bw halves
      3. invert seventh bit of intf id
    * implemented w `ipv6 address $addr/$prefix eui-64`
      - used w the addr as the prefix
* dynamic unicast addr config
  * dhcp: `ipv6 address dhcp`
  * slaac: `ipv6 address autoconfig`
* special r addrs
  - link local addrs
    * used for overhead an ring protocols
    * does not leave subnet ex. ndp (v6 ver of arp; neighbor discovery protocol)
    * routes to link local instead of formal
    * unicast, autogen 
    * prefix fe80::/10
    * config `ipv6 address $addr link-local $intf` and `ipv6 enable`
  - ipv6 multicast

name|addr|meaning|v4 equ
---|---|---|---
all nodes|ff02::1|all intf using v6 on that link|subnet broadcast addr
all r|ff02::2|all r on link|none
all ospf(-dr)|ff02::5-6|all ospf r| 224.0.0.5-6
ripng r|ff02::9|all ripng r|224.0.0.9
eigrpv6 r|ff02::a|all ...|224.0.0.10
dhcp relay aget|ff02::1:2|r acting as relay|none

    * solicited node mlticast
      - multicast, linklocal, calculated w v6 addr (last 6 digits), each host
        listens at this addr, there can be overlap bw hosts
      - listening to this addr is "joining" and means those multicast addr
        share the same "interest" thus how multicast addr can be specified to
different types of r and such
  - anycast addr
    1. 2 r config w same anycast addr
    2. in the future, other r route packet to closest one to complete a service
    * `ipv6 address $addr anycast`
  - misc
    * unknown ::, used when host does not know its ip yet
    * loopback ::1 
### 30. implement v6 addr on hosts
* ndp
  - slaac: uses to learn first part of addr + prefix len
  - r discovery: learn v6 addr of available ipv6 in subnet
  - duplicate addr detection (dad)
  - neighbor mac discovery: after pass dad use this (equ v4 arp)
  - r discovery
    * r solicitarion (rs): sent to all v6 local rs multicast addr ff02::2
    * r advertisement (ra): sends link local v6; unsolicited ff02::1, in
      response to rs, it is sent back to host
  - addr info for slaac discovery 
    * from the ra msg, it can calculate prefix from the given prefix length
      "/n"
  - neighbor link addr discovery
    *  neighbor solicitation (ns): asks for na w mac addr; sent to
       solicited-nod emulticast addr asso w target
    * neighbor adv (na): sent back to request host unicast addr or unsolicited
      to ff02::1
  - dad
    * essentially neighbor link discovery where query is its own addr
    * if it gets a response it is a duplicate
    * autocheck when link is first used and when link is set to up
* dynamic h config
  - dynamic config w stateful dhcp and ndp
  - stateful works like dhcpv4: trakcs info abt client leases, and knows info
    abt specific clients
    * like v4 it supplies unicast addr, prefix len, and dns servers but does
      not supply default r
    * default r supplied by ndp
    * relay agents
      - src: lnk local addr
      - dst: ff02::1:2 (all dhcp agents)
  - stateless: does not track per-client
    * stateful requires admin, config, and mgmt 
    * slaac allows for ip asmt wo stateful server 
    * host chooses ip:
      1. learn v6 refix used on link from any r w ndp rs/ra
      2. choose its own ipv6 addr by making up intf id to follow learned prefix
      3. before choosing addr, use dad to find dups
    * dhcp is only used to learn addr of dns servers
* v6 troubleshooting addrs
  - use trad cmds but like `ping6`
  - `traceroute6`
  - can also display ndp info `ndp -an`
### 31. implementing v6 routing
* connected and local ipv6 rs
  - added routes
    * addrs on connected intf
    * addrs of direct static config
    * config of ring protocol on r w same datalink (dynamic rs)
* how rs create routes based on config of intf v6 unicast addr
  1. rs create v6 routes cased in each unicast v6 addr in an intf
    * connected subnet routes
    * local host route 
  2. rs do not create routes based on link local addrs
  3. rs remove connected and local rs for an intf if the intf fails 
* static v6 routes
  - similar to v4 config
  - cna be seen `show ipv6 route $addr`
  - using next hop v6 addresses
    * same as v4
  - static default routes
    * no default route > packet discarded
  - can also make host to host routes
  - floating static routes
    * need to change admin distance to prefer routing protocols
  - default routes w slaac on r intf
    * `ipv6 address autoconfig default`
    * on getting a ndp ra msg, it builds its own intf addr and addes a local
      /128 route as it would for any interface, adds a connected routes, and
a default route is added

## IX. network device management
### 32. device management protocols
* syslog 
  - real time msgs can be displayed on anny console/terminal
  - storing log msgs
    * can send msgs w `logging {addr|hostname}`
  - severity lvls

keyword|numeral|desc
---|---|---
emergency|0|immediate axn
alert|1|sys unusable
critical|2|crit event
error|3|error event
warning|4|warning event
notif|5|normal more imp
informational|6|normal less imp
debug|7|requested by user debug

  - enable lvl logging w `logging {console|monitor|buffered|host
    {addr|hostname}} lvl-name|lvl-num`
  - debug cmd
    * gives engineer method of asking ios to monitor certain internal events
    * ex. `debug ip rip`
* network time protocol (ntp)
  - synchronizing timezones and time logs
  - `clock` cmds
  - ntp clients, servers, and client/server mode
    * ntp clients adjust based on server
    * ntp servers do not adjust
    * client/server does both
  - `ntp master` to act as server
  - ntp loopback intf 
    * better availability 
    * ensures route to server even if one intf fails
* analyzing topology w cdp and lldp
  - cisco discovery protocol
    * shows basic info abt neighbor wo needing to know pwds 
    * learns info from analyzing sent msgs
    * cisco proprietary
  - link layer discovery protocol
    * ieee defined standard
### 34. device security features
* securing ios pwds
  - `service password-encryption`
  - enable secret of a pwd to hash
    * enable algorithim type
  - on local machines can be made hash w `username $user secret $pwd`
* cisco device hardening
  - config login banners
  - secure unused switch intf 
    1. shutdown 
    2. `switchport mode access`
    3. assign port to an unused vlan intf
    4. assign native vlan to an unused vlan
  - ctrl telnet access w acls
  - firewalls
    * can also be used as filtering acl to create zones 
### 34. managing ios files
* ios fs
  - usually flash mem
  - ios fs (ifs)
    * opaque: interal fs for convenience of funx and cmds
    * netwk: external fs found on servers for ios cmds reference
    * disk: for flash
    * usbflash
    * nvram
* upgrading ios
  - place img in reachable ftp or tftp server or flash a usb
  - issue `copy` cmd from router to copy into flash mem 
    * ex. `copy tftp flash`
  - `show flash`
  - can also verify hash
* ios boot seq
  1. post prcs 
  2. r copies bootstrap pgm from rom into ram and runs ram
  3. bootstrap decides which ios img to load into ram 
  4. run startup-config file
* config register
  - ctl startup settings
* how to choose os
  - based on last hex digit in config register 
  - use `boot system` in global config to chg
  - if boot field=0 use rommon os, 1: load first ios file in mem, 2-f: try each
    boot system cmd in config and if those dont work load first ios img in mem
    * rommon > rom monitor
* password recovery
  1. boot rommon by interrupt boot or remove all flash mem
  2. set config reg to ignore startup-config `confreg 0x2142`
  3. boot router w ios to reset
* managing config files
  - backups manual
    1. copy running config to external server ex. `copy running-config tftp`
    2. to restore: copy it back and use `reload`
  - backup auto
    * `configure replace` lets you overwrite running-config completely
    * create archives

```
archive
path ftp://cow@192.168.0.1/
time-period 1440
write-memory
```

* `show version`
  - shows ver, place copied from, and ios boot img
### 35. ios license management 
* ios packaging
  - originally ios had diff ver for diff hardware
  - og packaging:
    * one combo of ios features for every possibility
    * all have the ip base package w additional security, data, and voice
      packages
  - new packaging:
    * "universal"
    * all features in one set but still diff sets per model
* ios software activation w universal imgs
  - ip base is auto enabled
  - feature sets are need to be activated
  - legal rights are verified
* managing software activation w cisco license mgr
  - cisco license mgr (csm)
    * communicates w cisco product license reg 
    * takes input info abt feature licenses purchased from resellers
    * communicates w companys rs and switches to install license keys
  - manual activationi paid-for
    * `show license udi` "universal dev id"
    * input udi and pak (product access key) at cisco's website
    * cp license key file to r and reload
  - manual right-to-use
    * `license install $dir`
    * need to reload modules for right-to-use `license boot module c2900
      technology-package $pkgname`

